import json
import os
from dotenv import load_dotenv
from openai import OpenAI
from models.schemas import ResumeOutput

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """
    You are an expert ATS resume optimizer.

    Rules:
    1. Add skills if not already present.
    2. Optimize wording to match the job description.
    3. Summary must be a SINGLE paragraph.
    4. Summary should be 50-80 words.
    5. Work experience must contain 2-3 bullet points.
    6. Every bullet should be one sentence of 12-15 words each.
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
    18. Prefer 3-5 skill categories total and 5-10 skills per category.
    19. Include only skills that are present in the resume, strongly implied by experience, or directly requested by the job description.
"""


class AIOptimizer:
    @staticmethod
    def optimize(jd_text: str, current_resume: ResumeOutput) -> ResumeOutput:
        prompt = f"""
            JOB DESCRIPTION:
            {jd_text}

            CURRENT RESUME DATA:
            {current_resume.model_dump_json(indent=2)}

            Rewrite the resume to better match the job description.
            For "skills", choose category names dynamically from the job description.
            Do not use a hardcoded category set. It is acceptable to keep stable
            categories like "Core Skills" or "Programming Languages" when they fit.
            Keep skill lists concise, deduplicated, and ordered by relevance.
            Return JSON in EXACTLY this format:

            {{
                "summary": "",

                "kpit_se": [],
                "kpit_ase": [],
                "kpit_trainee": [],

                "nic": [],
                "dit": [],

                "skills": {{
                    "Dynamic Category Name": []
                }},

                "project_dat": [],
                "project_gpt": [],
                "project_acg": [],
                "project_cms": []
            }}
        """

        response = client.chat.completions.create(
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

        data = json.loads(response.choices[0].message.content)

        return ResumeOutput(**data)