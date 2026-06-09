from fastapi import APIRouter
from app.api.v1.endpoints import resume, ats


api_router = APIRouter()

api_router.include_router(resume.router, prefix="/resume", tags=["resume"])
api_router.include_router(ats.router, prefix="/ats", tags=["ats"])

@api_router.get("/info", tags=["info"])
def get_info():
    return {
        "status": "online",
        "supported_features": [
            "resume_parsing",
            "postgresql_metadata_storage",
            "chromadb_vector_search",
            "ats_scoring"
        ]
    }
