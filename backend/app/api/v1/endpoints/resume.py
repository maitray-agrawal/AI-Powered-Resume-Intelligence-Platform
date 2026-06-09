from fastapi import APIRouter, Depends, UploadFile, File, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.resume import ResumeUploadResponse
from app.services.resume import ResumeService

router = APIRouter()


@router.post(
    "/upload",
    response_model=ResumeUploadResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Upload and parse resume",
    description="Uploads a PDF or DOCX resume, stores it locally, extracts text, and indexes metadata."
)
def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    return ResumeService.save_and_parse_resume(db=db, file=file)
