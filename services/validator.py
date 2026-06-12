from models.schemas import ResumeOutput


class ResumeValidator:
    @staticmethod
    def validate(resume: ResumeOutput):
        ResumeValidator._validate_summary(resume.summary)
        ResumeValidator._validate_bullets(resume.kpit_se, "KPIT_SE")
        ResumeValidator._validate_bullets(resume.kpit_ase, "KPIT_ASE")
        ResumeValidator._validate_bullets(resume.kpit_trainee, "KPIT_TRAINEE")
        ResumeValidator._validate_bullets(resume.nic, "NIC")
        ResumeValidator._validate_bullets(resume.dit, "DIT")
        ResumeValidator._validate_projects(resume.project_dat)
        ResumeValidator._validate_projects(resume.project_gpt)
        ResumeValidator._validate_projects(resume.project_acg)
        ResumeValidator._validate_projects(resume.project_cms)

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