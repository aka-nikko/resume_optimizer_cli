from pydantic import BaseModel
from typing import Dict, List


class ResumeOutput(BaseModel):
    summary: str

    experience_1: List[str]
    experience_2: List[str]
    experience_3: List[str]

    experience_4: List[str]
    experience_5: List[str]

    skills: Dict[str, List[str]]

    project_1: List[str]
    project_2: List[str]
    project_3: List[str]
    project_4: List[str]