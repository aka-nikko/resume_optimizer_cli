from models.schemas import ResumeOutput


class ResumeValidator:
    @staticmethod
    def validate(resume: ResumeOutput):
        ResumeValidator._validate_summary(resume.summary)
        ResumeValidator._validate_bullets(resume.experience_1, "EXPERIENCE_1")
        ResumeValidator._validate_bullets(resume.experience_2, "EXPERIENCE_2")
        ResumeValidator._validate_bullets(resume.experience_3, "EXPERIENCE_3")
        ResumeValidator._validate_bullets(resume.experience_4, "EXPERIENCE_4")
        ResumeValidator._validate_bullets(resume.experience_5, "EXPERIENCE_5")
        ResumeValidator._validate_projects(resume.project_1)
        ResumeValidator._validate_projects(resume.project_2)
        ResumeValidator._validate_projects(resume.project_3)
        ResumeValidator._validate_projects(resume.project_4)

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