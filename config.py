from typing import Pattern
import re

# DOCX / writer settings
FONT_SIZE = 10
PLACEHOLDER_PATTERN = r"\{\{\s*([^{}]+?)\s*\}\}"
EXPERIENCE_PLACEHOLDER = r"^EXPERIENCE_(\d+)$"
PROJECT_PLACEHOLDER = r"^PROJECT_(\d+)$"
MARKDOWN_BOLD_PATTERN = r"(\*\*.*?\*\*)"
REQUIRED_PLACEHOLDERS = ["SUMMARY", "SKILLS"]

# Bullet formatting (inches/points or numeric)
BULLET_LEFT_INDENT_INCHES = 0.2
BULLET_FIRST_LINE_INDENT_INCHES = 0
BULLET_LINE_SPACING = 0.9
BULLET_SPACE_BEFORE_PT = 0
BULLET_SPACE_AFTER_PT = 0

# Resume validation rules
SUMMARY_MIN_WORDS = 50
SUMMARY_MAX_WORDS = 65
EXPERIENCE_MIN_BULLETS = 2
EXPERIENCE_MAX_BULLETS = 3
PROJECT_BULLETS = 2

# Skill categories
PROGRAMMING_LANGUAGES_CATEGORY = "Programming Languages"

# AI / OpenAI settings
AI_MODEL = "gpt-5"
AI_SYSTEM_PROMPT = """
    You are an expert ATS resume optimizer.

    Rules:
    1. Add skills if not already present.
    2. Optimize wording to match the job description.
    3. Summary must be a SINGLE paragraph.
    4. Summary should be 50-65 words.
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
    20. Skills must include "Programming Languages" as the first category.
"""

DEFAULT_OUTPUT_NAME = "output_resume.docx"
