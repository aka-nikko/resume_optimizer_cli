from models.schemas import ResumeOutput
from config import (
    SUMMARY_MIN_WORDS,
    SUMMARY_MAX_WORDS,
    EXPERIENCE_MIN_BULLETS,
    EXPERIENCE_MAX_BULLETS,
    PROJECT_BULLETS,
)


class ResumeValidator:
    @staticmethod
    def validate(resume: ResumeOutput, section_counts=None):
        section_counts = section_counts or {}
        experience_count = section_counts.get("experiences", len(resume.experiences))
        project_count = section_counts.get("projects", len(resume.projects))

        if experience_count < 0 or project_count < 0:
            raise ValueError("Template section counts cannot be negative")

        ResumeValidator._validate_summary(resume.summary)
        ResumeValidator._validate_section_count(resume.experiences, experience_count, "experience")
        ResumeValidator._validate_section_count(resume.projects, project_count, "project")
        ResumeValidator._validate_skills(resume.skills)

        for index, bullets in enumerate(resume.experiences[:experience_count], start=1):
            ResumeValidator._validate_bullets(bullets, f"EXPERIENCE_{index}")

        for index, project in enumerate(resume.projects[:project_count], start=1):
            ResumeValidator._validate_projects(project, f"PROJECT_{index}")

    @staticmethod
    def _validate_section_count(sections, expected_count, section_type):
        if len(sections) < expected_count:
            raise ValueError(
                f"Template requires {expected_count} {section_type} sections, "
                f"but resume only has {len(sections)}"
            )

    @staticmethod
    def _validate_summary(summary):
        summary = summary.strip()

        if "\n" in summary:
            raise ValueError("Summary must be a paragraph")

        words = len(summary.split())

        if words < SUMMARY_MIN_WORDS:
            raise ValueError(f"Summary too short: expected {SUMMARY_MIN_WORDS}-{SUMMARY_MAX_WORDS} words, got {words}")

        if words > SUMMARY_MAX_WORDS:
            raise ValueError(f"Summary too long: expected {SUMMARY_MIN_WORDS}-{SUMMARY_MAX_WORDS} words, got {words}")

    @staticmethod
    def _validate_skills(skills):
        if not skills:
            raise ValueError("Skills section must not be empty")

        for category, skill_list in skills.items():
            if not category.strip():
                raise ValueError("Skill category names must not be empty")

            if not skill_list:
                raise ValueError(f"Skill category '{category}' must contain at least one skill")

    @staticmethod
    def _validate_bullets(bullets, section):
        if len(bullets) < EXPERIENCE_MIN_BULLETS:
            raise ValueError(f"{section} requires at least {EXPERIENCE_MIN_BULLETS} bullets")

        if len(bullets) > EXPERIENCE_MAX_BULLETS:
            raise ValueError(f"{section} requires {EXPERIENCE_MIN_BULLETS}-{EXPERIENCE_MAX_BULLETS} bullets")

        for bullet_index, bullet in enumerate(bullets, start=1):
            if not bullet.strip():
                raise ValueError(f"{section} bullet {bullet_index} must not be empty")

    @staticmethod
    def _validate_projects(project, section):
        if len(project) != PROJECT_BULLETS:
            raise ValueError(f"{section} requires exactly {PROJECT_BULLETS} bullets")

        for bullet_index, bullet in enumerate(project, start=1):
            if not bullet.strip():
                raise ValueError(f"{section} bullet {bullet_index} must not be empty")