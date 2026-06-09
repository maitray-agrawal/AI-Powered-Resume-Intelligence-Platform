from pydantic import BaseModel
from typing import List, Optional


class ResumeDataInput(BaseModel):
    name: Optional[str] = "Unknown"
    email: Optional[str] = ""
    phone: Optional[str] = ""
    skills: List[str] = []
    education: Optional[str] = ""
    experience: Optional[str] = ""
    projects: Optional[str] = ""


class ATSScoreRequest(BaseModel):
    resume: ResumeDataInput
    job_description_keywords: Optional[List[str]] = None


class ATSScoreResponse(BaseModel):
    keyword_score: float
    section_score: float
    length_score: float
    overall_score: float
    findings: List[str]
    suggestions: List[str]
