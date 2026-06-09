from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional, Any


class ResumeVersionResponse(BaseModel):
    id: UUID
    version_number: int
    file_name: str
    file_path: str
    created_at: datetime

    class Config:
        from_attributes = True


class ResumeUploadResponse(BaseModel):
    id: UUID
    user_id: UUID
    title: str
    created_at: datetime
    updated_at: datetime
    latest_version: ResumeVersionResponse

    class Config:
        from_attributes = True
