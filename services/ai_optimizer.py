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

    1. Never fabricate experience.
    2. Never invent projects.
    3. Add skills if not already present.
    4. Optimize wording to match the job description.
    5. Summary must be a SINGLE paragraph.
    6. Summary should be 50-80 words.
    7. Work experience must contain 2-3 bullet points.
    8. Every bullet should be one sentence of 12-15 words each.
    9. Every project must contain exactly 2 bullet points.
    10. Keep technical accuracy.
    11. Prioritize ATS keywords naturally.
    12. Return ONLY valid JSON.
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
            Return JSON in EXACTLY this format:

            {{
                "summary": "",

                "kpit_se": [],
                "kpit_ase": [],
                "kpit_trainee": [],

                "nic": [],
                "dit": [],

                "skills": {{
                    "Embedded & Automotive": [],
                    "Software Engineering": [],
                    "Backend & Full Stack": [],
                    "AI & Automation": []
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