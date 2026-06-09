import os
import shutil
import uuid
from fastapi import UploadFile, HTTPException, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models import User, Resume, ResumeVersion
from app.services.vector_db import vector_db_service


class ResumeService:
    @staticmethod
    def get_or_create_default_user(db: Session) -> User:
        """
        Retrieves the first user from the database or creates a default system user
        if the table is currently empty.
        """
        user = db.query(User).first()
        if not user:
            user = User(
                email="default_recruiter@example.com",
                hashed_password="placeholder_hash_value",
                is_active=True
            )
            db.add(user)
            db.commit()
            db.refresh(user)
        return user

    @classmethod
    def save_and_parse_resume(cls, db: Session, file: UploadFile) -> Resume:
        filename = file.filename or "resume.pdf"
        _, ext = os.path.splitext(filename)
        ext = ext.lower()
        if ext not in ['.pdf', '.docx']:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported file format '{ext}'. Only .pdf and .docx files are permitted."
            )

        # Ensure upload directory exists
        upload_dir = settings.UPLOAD_DIR
        os.makedirs(upload_dir, exist_ok=True)

        # Generate unique local filename
        unique_id = uuid.uuid4()
        saved_filename = f"{unique_id}{ext}"
        file_path = os.path.join(upload_dir, saved_filename)

        # Save file locally
        try:
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to write file locally: {str(e)}"
            )

        # Extract and parse structure from file
        try:
            from app.services.parser_service import ResumeParserService
            parsed_data = ResumeParserService.parse_resume(file_path)
            raw_text = ResumeParserService.extract_text(file_path)
        except Exception as e:
            if os.path.exists(file_path):
                os.remove(file_path)
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Parsing error: {str(e)}"
            )

        # Get or create default user
        user = cls.get_or_create_default_user(db)

        # Save records in database
        try:
            # Create parent Resume
            resume = Resume(
                user_id=user.id,
                title=filename
            )
            db.add(resume)
            db.commit()
            db.refresh(resume)

            # Create ResumeVersion record
            version = ResumeVersion(
                resume_id=resume.id,
                version_number=1,
                file_name=filename,
                file_path=file_path,
                raw_text=raw_text,
                structured_data={
                    "file_size_bytes": os.path.getsize(file_path),
                    "character_count": len(raw_text),
                    "parsed_structure": parsed_data
                }
            )
            db.add(version)
            db.commit()
            db.refresh(version)
            
            # Link version reference to return object dynamically
            resume.latest_version = version

        except Exception as e:
            if os.path.exists(file_path):
                os.remove(file_path)
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database logging failure: {str(e)}"
            )

        # Index in ChromaDB (graceful fallback if offline)
        try:
            mock_embedding = [0.1] * 128
            vector_db_service.add_vectors(
                collection_name="resumes",
                ids=[str(version.id)],
                embeddings=[mock_embedding],
                documents=[raw_text],
                metadatas=[{
                    "resume_id": str(resume.id),
                    "filename": filename
                }]
            )
        except Exception as err:
            print(f"ChromaDB index warning: {str(err)}")

        return resume
