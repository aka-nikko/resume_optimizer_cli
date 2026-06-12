from models.schemas import ResumeOutput


class ResumeValidator:
    @staticmethod
    def validate(resume: ResumeOutput, section_counts=None):
        section_counts = section_counts or {}
        experience_count = section_counts.get("experiences", len(resume.experiences))
        project_count = section_counts.get("projects", len(resume.projects))

        ResumeValidator._validate_summary(resume.summary)
        ResumeValidator._validate_section_count(resume.experiences, experience_count, "experience")
        ResumeValidator._validate_section_count(resume.projects, project_count, "project")

        for index, bullets in enumerate(resume.experiences[:experience_count], start=1):
            ResumeValidator._validate_bullets(bullets, f"EXPERIENCE_{index}")

        for project in resume.projects[:project_count]:
            ResumeValidator._validate_projects(project)

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

        if words < 50:
            raise ValueError("Summary too short")

        if words > 80:
            raise ValueError("Summary too long")

    @staticmethod
    def _validate_bullets(bullets, section):
        if len(bullets) < 2:
            raise ValueError(f"{section} requires 2-3 bullets")

        if len(bullets) > 4:
            raise ValueError(f"{section} requires 2-4 bullets")

    @staticmethod
    def _validate_projects(project):
        if len(project) != 2:
            raise ValueError("Project requires exactly 2 bullets")