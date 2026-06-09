from fastapi import APIRouter, status
from app.schemas.llm import (
    ResumeImproveRequest,
    ResumeImproveResponse,
    ResumeRewriteRequest,
    ResumeRewriteResponse,
    InterviewQuestionsRequest,
    InterviewQuestionsResponse,
    CoverLetterRequest,
    CoverLetterResponse
)
from app.services.llm_service import GeminiLLMService

router = APIRouter()


@router.post(
    "/improvement",
    response_model=ResumeImproveResponse,
    status_code=status.HTTP_200_OK,
    summary="Generate resume improvement tips",
    description="Uses Gemini to analyze the candidate resume and optional target Job Description, outputting 3 core actionable optimization tips."
)
def get_resume_improvement(request: ResumeImproveRequest):
    suggestions = GeminiLLMService.resume_improvement(
        resume_text=request.resume_text,
        job_description=request.job_description
    )
    return {"improvements": suggestions}


@router.post(
    "/rewrite",
    response_model=ResumeRewriteResponse,
    status_code=status.HTTP_200_OK,
    summary="Redraft resume sections for a target role",
    description="Uses Gemini to rewrite specific sections of a candidate resume to optimize relevance for a target professional role."
)
def rewrite_resume_sections(request: ResumeRewriteRequest):
    rewrites = GeminiLLMService.resume_rewrite(
        resume_text=request.resume_text,
        target_role=request.target_role,
        sections_to_rewrite=request.sections_to_rewrite
    )
    return {"rewritten_sections": rewrites}


@router.post(
    "/interview-questions",
    response_model=InterviewQuestionsResponse,
    status_code=status.HTTP_200_OK,
    summary="Generate tailored interview questions",
    description="Uses Gemini to generate mock interview questions, rationales, and suggested response approaches mapped to the candidate resume and JD."
)
def get_interview_questions(request: InterviewQuestionsRequest):
    questions = GeminiLLMService.interview_questions(
        resume_text=request.resume_text,
        job_description=request.job_description
    )
    return {"questions": questions}


@router.post(
    "/cover-letter",
    response_model=CoverLetterResponse,
    status_code=status.HTTP_200_OK,
    summary="Tailor a cover letter to a job description",
    description="Uses Gemini to generate a complete cover letter linking candidate experience to Job Description requirements."
)
def generate_cover_letter(request: CoverLetterRequest):
    letter = GeminiLLMService.cover_letter(
        resume_text=request.resume_text,
        job_description=request.job_description
    )
    return {"cover_letter": letter}
