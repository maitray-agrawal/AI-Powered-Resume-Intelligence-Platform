from fastapi import APIRouter
from app.api.v1.endpoints import resume, ats, jd_matcher, llm, rag, agents, analytics

api_router = APIRouter()

api_router.include_router(resume.router, prefix="/resume", tags=["resume"])
api_router.include_router(ats.router, prefix="/ats", tags=["ats"])
api_router.include_router(jd_matcher.router, prefix="/jd-matcher", tags=["jd-matcher"])
api_router.include_router(llm.router, prefix="/llm", tags=["llm"])
api_router.include_router(rag.router, prefix="/rag", tags=["rag"])
api_router.include_router(agents.router, prefix="/agents", tags=["agents"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["analytics"])

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
