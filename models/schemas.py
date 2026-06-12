from pydantic import BaseModel
from typing import Dict, List


class ResumeOutput(BaseModel):
    summary: str

    kpit_se: List[str]
    kpit_ase: List[str]
    kpit_trainee: List[str]

    nic: List[str]
    dit: List[str]

    skills: Dict[str, List[str]]

    project_dat: List[str]
    project_gpt: List[str]
    project_acg: List[str]
    project_cms: List[str]