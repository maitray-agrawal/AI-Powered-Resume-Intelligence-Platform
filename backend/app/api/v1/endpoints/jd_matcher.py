from fastapi import APIRouter, status
from app.schemas.jd_matcher import JDMatchRequest, JDMatchResponse
from app.services.jd_matcher import JDMatcherService

router = APIRouter()


@router.post(
    "/match",
    response_model=JDMatchResponse,
    status_code=status.HTTP_200_OK,
    summary="Semantically match resume to Job Description",
    description="Uses sentence-transformers all-MiniLM-L6-v2 model to calculate cosine similarities between resume and JD texts and skill lists."
)
def match_jd(request: JDMatchRequest):
    result = JDMatcherService.calculate_semantic_match(
        resume_text=request.resume_text,
        resume_skills=request.resume_skills,
        job_description_text=request.job_description_text,
        job_description_skills=request.job_description_skills
    )
    return result
