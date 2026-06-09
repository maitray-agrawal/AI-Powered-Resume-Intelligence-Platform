import os
import shutil
import tempfile
import pytest
from app.core.config import settings
from app.services.mlflow_service import MLflowTrackingService


@pytest.fixture(scope="module")
def temp_mlflow_dir():
    """Create a temporary directory for MLflow tracking during tests."""
    temp_dir = tempfile.mkdtemp()
    original_uri = settings.MLFLOW_TRACKING_URI
    settings.MLFLOW_TRACKING_URI = f"sqlite:///{temp_dir.replace('\\', '/')}/mlflow.db"
    
    # Reset initialization flag for the test
    MLflowTrackingService._initialized = False
    
    yield temp_dir
    
    # Restore original setting
    settings.MLFLOW_TRACKING_URI = original_uri
    MLflowTrackingService._initialized = False
    
    # Cleanup temp directory
    try:
        shutil.rmtree(temp_dir)
    except Exception:
        pass


def test_mlflow_initialization(temp_mlflow_dir):
    """Test that MLflow tracking service initializes successfully."""
    success = MLflowTrackingService.initialize()
    assert success is True
    assert MLflowTrackingService._initialized is True


def test_log_ats_score(temp_mlflow_dir):
    """Test logging ATS scoring metrics to MLflow."""
    # This should not raise any exceptions
    MLflowTrackingService.log_ats_score(
        resume_name="Test_Resume.pdf",
        overall_score=85.5,
        metrics={"keyword_score": 90.0, "section_score": 80.0, "length_score": 80.0},
        params={"skills_count": 12, "job_keywords_count": 8},
        findings=["Found 12 skills", "Word count is good"],
        suggestions=["Add PostgreSQL to skills"]
    )


def test_log_jd_match(temp_mlflow_dir):
    """Test logging Job Description match metrics to MLflow."""
    MLflowTrackingService.log_jd_match(
        resume_skills_count=10,
        jd_skills_count=15,
        overall_score=75.5,
        metrics={"resume_similarity": 0.72, "skill_similarity": 0.79},
        matched_skills=["Python", "FastAPI", "SQL"],
        missing_skills=["Docker", "Kubernetes"]
    )


def test_log_rag_chat(temp_mlflow_dir):
    """Test logging RAG chatbot Q&A interactions to MLflow."""
    import uuid
    resume_id = uuid.uuid4()
    MLflowTrackingService.log_rag_chat(
        resume_id=str(resume_id),
        query="What is the candidate's experience in Python?",
        answer="The candidate has 4 years of experience using Python for backend development.",
        source_count=3
    )


def test_log_agent_workflow(temp_mlflow_dir):
    """Test logging LangGraph multi-agent workflow results to MLflow."""
    workflow_result = {
        "ats_feedback": {"score": 85, "formatting_score": 90},
        "recruiter_feedback": {"fit_rating": 4.5, "hiring_verdict": "Shortlist"},
        "reviewer_feedback": {"writing_score": 88},
        "advisor_feedback": {"recommended_roles": ["Backend Engineer"]},
        "consolidated_report": {
            "fit_percentage": 82.5,
            "summary": "Overall strong backend developer."
        }
    }
    MLflowTrackingService.log_agent_workflow(
        workflow_result=workflow_result,
        job_description_length=250
    )
