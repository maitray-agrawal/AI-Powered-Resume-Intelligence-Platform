from fastapi import APIRouter, status
from app.schemas.ats import ATSScoreRequest, ATSScoreResponse
from app.services.ats_service import ATSEngineService

router = APIRouter()


@router.post(
    "/score",
    response_model=ATSScoreResponse,
    status_code=status.HTTP_200_OK,
    summary="Compute ATS resume compatibility score",
    description="Accepts parsed resume JSON structure and computes keyword matches, section completeness, and document length scores."
)
def score_resume(request: ATSScoreRequest):
    result = ATSEngineService.calculate_ats_score(
        resume=request.resume,
        job_keywords=request.job_description_keywords
    )
    return result
