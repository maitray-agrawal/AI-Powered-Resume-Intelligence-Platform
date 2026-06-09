from pydantic import BaseModel
from uuid import UUID
from typing import List


class RAGIngestRequest(BaseModel):
    resume_id: UUID
    resume_text: str


class RAGIngestResponse(BaseModel):
    success: bool
    num_chunks: int


class RAGChatRequest(BaseModel):
    resume_id: UUID
    query: str


class RAGChatResponse(BaseModel):
    answer: str
    sources: List[str]
