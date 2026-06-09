from pydantic import BaseModel
from uuid import UUID
from typing import Optional, Dict, Any


class AgentAnalyzeRequest(BaseModel):
    resume_id: UUID
    job_description: Optional[str] = None


class AgentAnalyzeResponse(BaseModel):
    resume_id: UUID
    ats_feedback: Dict[str, Any]
    recruiter_feedback: Dict[str, Any]
    reviewer_feedback: Dict[str, Any]
    advisor_feedback: Dict[str, Any]
    consolidated_report: Dict[str, Any]
