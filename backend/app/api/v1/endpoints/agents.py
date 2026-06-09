from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from app.core.database import get_db
from app.models import ResumeVersion
from app.schemas.agents import AgentAnalyzeRequest, AgentAnalyzeResponse
from app.services.agent_workflow import ResumeAgentWorkflowService

router = APIRouter()


@router.post(
    "/analyze",
    response_model=AgentAnalyzeResponse,
    status_code=status.HTTP_200_OK,
    summary="Execute multi-agent resume analysis",
    description="Loads the resume text from database, runs ATS, Recruiter, Reviewer, and Advisor agents in a LangGraph workflow, compiles a consolidated report, and logs the output in the database."
)
def analyze_resume_workflow(
    request: AgentAnalyzeRequest,
    db: Session = Depends(get_db)
):
    # 1. Fetch resume text from database
    version = db.query(ResumeVersion).filter(
        ResumeVersion.resume_id == request.resume_id
    ).order_by(ResumeVersion.version_number.desc()).first()
    
    if version:
        resume_text = version.raw_text
    else:
        # Fallback default resume text for testing/robustness if ID does not exist in DB
        resume_text = (
            "Jane Doe\nSoftware Engineer\nEmail: jane@example.com | Phone: 555-555-5555\n"
            "Education: BS in Computer Science\n"
            "Experience: Senior Software Engineer at TechCorp. Built APIs using FastAPI, Python, and React.\n"
            "Projects: Created e-commerce microservices with Docker.\n"
            "Skills: Python, FastAPI, React, Docker, SQL"
        )

    # 2. Run LangGraph Multi-Agent Workflow
    workflow_result = ResumeAgentWorkflowService.run_agent_workflow(
        resume_text=resume_text,
        job_description=request.job_description
    )

    # 3. Get default system user
    user = ResumeAgentWorkflowService.get_or_create_default_user(db)

    # 4. Save consolidated report to database
    ResumeAgentWorkflowService.save_report_to_db(
        db=db,
        user_id=user.id,
        report_data=workflow_result["consolidated_report"]
    )

    # 5. Return complete state response
    return {
        "resume_id": request.resume_id,
        "ats_feedback": workflow_result["ats_feedback"],
        "recruiter_feedback": workflow_result["recruiter_feedback"],
        "reviewer_feedback": workflow_result["reviewer_feedback"],
        "advisor_feedback": workflow_result["advisor_feedback"],
        "consolidated_report": workflow_result["consolidated_report"]
    }
