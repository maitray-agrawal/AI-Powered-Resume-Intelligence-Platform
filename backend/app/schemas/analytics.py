from pydantic import BaseModel
from typing import List


class ATSScoreHistoryItem(BaseModel):
    date: str
    score: float


class JDMatchHistoryItem(BaseModel):
    role: str
    score: float


class SkillGapItem(BaseModel):
    skill: str
    frequency: int


class AgentScoreItem(BaseModel):
    agent: str
    score: float


class DashboardAnalyticsResponse(BaseModel):
    ats_score_history: List[ATSScoreHistoryItem]
    jd_match_history: List[JDMatchHistoryItem]
    skill_gaps: List[SkillGapItem]
    agent_scores: List[AgentScoreItem]
