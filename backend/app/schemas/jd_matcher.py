from pydantic import BaseModel
from typing import List


class JDMatchRequest(BaseModel):
    resume_text: str
    resume_skills: List[str]
    job_description_text: str
    job_description_skills: List[str]


class JDMatchResponse(BaseModel):
    resume_similarity: float
    skill_similarity: float
    match_percentage: float
