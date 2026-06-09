from pydantic import BaseModel
from typing import List, Optional, Dict, Any


class ResumeImproveRequest(BaseModel):
    resume_text: str
    job_description: Optional[str] = None


class ResumeImproveResponse(BaseModel):
    improvements: List[str]


class ResumeRewriteRequest(BaseModel):
    resume_text: str
    target_role: str
    sections_to_rewrite: List[str]


class ResumeRewriteResponse(BaseModel):
    rewritten_sections: Dict[str, str]


class InterviewQuestionsRequest(BaseModel):
    resume_text: str
    job_description: str


class InterviewQuestionItem(BaseModel):
    question: str
    rationale: str
    suggested_approach: str


class InterviewQuestionsResponse(BaseModel):
    questions: List[InterviewQuestionItem]


class CoverLetterRequest(BaseModel):
    resume_text: str
    job_description: str


class CoverLetterResponse(BaseModel):
    cover_letter: str
