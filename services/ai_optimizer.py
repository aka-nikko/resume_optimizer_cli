import json
import os
from dotenv import load_dotenv
from json import JSONDecodeError
from openai import OpenAI, OpenAIError
from pydantic import ValidationError
from models.schemas import ResumeOutput

load_dotenv()

SYSTEM_PROMPT = """
    You are an expert ATS resume optimizer.

    Rules:
    1. Add skills if not already present.
    2. Optimize wording to match the job description.
    3. Summary must be a SINGLE paragraph.
    4. Summary should be 50-65 words.
    5. Work experience must contain 2-3 bullet points.
    6. Every bullet should be one sentence of 12-14 words each.
    7. Every project must contain exactly 2 bullet points.
    8. Keep technical accuracy.
    9. Prioritize ATS keywords naturally.
    10. Return ONLY valid JSON.
    11. Bold important ATS keywords using markdown.
        Example:
        Developed **ADAS** features for **QNX-based systems**.
    12. Do not bold entire sentences.
    13. Bold 1-3 important terms per line/sentence.
    14. Keep the skills section focused and relevant to the job description.
    15. Use dynamic skill categories based on the job description and resume context.
    16. Core Skills and Programming Languages may be reused as stable categories when useful.
    17. Do not force unrelated categories or exhaustive keyword dumps.
    18. Prefer 3-4 skill categories total and 5-10 skills per category.
    19. Include only skills that are present in the resume, strongly implied by experience, or directly requested by the job description.
    20. Skills must include "Programming Languages" as the first category.
"""


class AIOptimizer:
    @staticmethod
    def get_client():
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY is missing. Add it to .env or your environment.")

        return OpenAI(api_key=api_key)

    @staticmethod
    def optimize(jd_text: str, current_resume: ResumeOutput, section_counts=None) -> ResumeOutput:
        if not jd_text or not jd_text.strip():
            raise ValueError("Job description text must not be empty.")

        section_counts = section_counts or {}
        experience_count = section_counts.get("experiences", len(current_resume.experiences))
        project_count = section_counts.get("projects", len(current_resume.projects))
        response_example = {
            "summary": "",
            "experiences": [[] for _ in range(experience_count)],
            "skills": {
                "Programming Languages": [],
                "Dynamic Category Name": []
            },
            "projects": [[] for _ in range(project_count)],
        }

        prompt = f"""
            JOB DESCRIPTION:
            {jd_text}

            CURRENT RESUME DATA:
            {current_resume.model_dump_json(indent=2)}

            Rewrite the resume to better match the job description.
            Keep "Programming Languages" as the first skills category.
            For "skills", choose category names dynamically from the job description.
            Do not use a hardcoded category set. It is acceptable to keep stable
            categories like "Core Skills" or "Programming Languages" when they fit.
            Keep skill lists concise, deduplicated, and ordered by relevance.
            Return exactly {experience_count} experience sections in "experiences".
            Return exactly {project_count} project sections in "projects".
            Return JSON in EXACTLY this format:

            {json.dumps(response_example, indent=4)}
        """

        try:
            response = AIOptimizer.get_client().chat.completions.create(
                model="gpt-5",
                messages=[
                    {
                        "role": "system",
                        "content": SYSTEM_PROMPT
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                response_format={
                    "type": "json_object"
                }
            )
        except OpenAIError as exc:
            raise RuntimeError(f"OpenAI request failed: {exc}") from exc

        if not response.choices:
            raise RuntimeError("OpenAI returned no choices.")

        content = response.choices[0].message.content
        if not content:
            raise RuntimeError("OpenAI returned an empty response.")

        try:
            data = json.loads(content)
        except JSONDecodeError as exc:
            raise RuntimeError("OpenAI returned invalid JSON.") from exc

        try:
            resume = ResumeOutput(**data)
        except ValidationError as exc:
            raise RuntimeError(f"OpenAI response did not match the resume schema: {exc}") from exc

        language_category = ResumeOutput.PROGRAMMING_LANGUAGES_CATEGORY
        has_language_category = any(
            category.casefold() == language_category.casefold()
            for category in resume.skills
        )
        if not has_language_category and language_category in current_resume.skills:
            resume.skills = ResumeOutput.order_skill_categories(
                {language_category: current_resume.skills[language_category], **resume.skills}
            )

        if len(resume.experiences) != experience_count:
            raise RuntimeError(
                f"OpenAI returned {len(resume.experiences)} experience sections; "
                f"template requires {experience_count}."
            )

        if len(resume.projects) != project_count:
            raise RuntimeError(
                f"OpenAI returned {len(resume.projects)} project sections; "
                f"template requires {project_count}."
            )

        return resume
