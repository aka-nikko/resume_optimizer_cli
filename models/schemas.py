from typing import Dict, List

from pydantic import BaseModel, Field, field_validator


class ResumeOutput(BaseModel):
    summary: str
    experiences: List[List[str]] = Field(default_factory=list)
    skills: Dict[str, List[str]] = Field(default_factory=dict)
    projects: List[List[str]] = Field(default_factory=list)

    @field_validator("summary")
    @classmethod
    def summary_must_not_be_empty(cls, value):
        if not value or not value.strip():
            raise ValueError("Summary must not be empty")

        return value.strip()

    @field_validator("experiences", "projects")
    @classmethod
    def sections_must_contain_bullets(cls, value):
        normalized_sections = []

        for section_index, section in enumerate(value, start=1):
            bullets = [bullet.strip() for bullet in section if bullet and bullet.strip()]
            if not bullets:
                raise ValueError(f"Section {section_index} must contain at least one bullet")

            normalized_sections.append(bullets)

        return normalized_sections

    @field_validator("skills")
    @classmethod
    def skills_must_have_categories(cls, value):
        normalized_skills = {}

        for category, skills in value.items():
            category_name = category.strip() if category else ""
            if not category_name:
                raise ValueError("Skill category names must not be empty")

            skill_values = [skill.strip() for skill in skills if skill and skill.strip()]
            if not skill_values:
                raise ValueError(f"Skill category '{category_name}' must contain at least one skill")

            normalized_skills[category_name] = list(dict.fromkeys(skill_values))

        return normalized_skills
