from pydantic import BaseModel
from typing import Dict, List


class ResumeOutput(BaseModel):
    summary: str
    experiences: List[List[str]]
    skills: Dict[str, List[str]]
    projects: List[List[str]]