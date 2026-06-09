import pytest
import uuid
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models import AgentReport, ResumeVersion
from app.services.agent_workflow import (
    ResumeAgentWorkflowService,
    ats_expert_node,
    recruiter_node,
    resume_reviewer_node,
    career_advisor_node,
    consolidation_node
)


def test_agent_nodes_fallback():
    # Verify node fallbacks function properly when offline
    state = {
        "resume_text": "Experienced Python Developer",
        "job_description": "We need Python developer",
        "ats_feedback": {},
        "recruiter_feedback": {},
        "reviewer_feedback": {},
        "advisor_feedback": {},
        "consolidated_report": {}
    }
    
    # 1. ATS Expert Node
    res = ats_expert_node(state)
    assert "ats_feedback" in res
    assert "formatting_score" in res["ats_feedback"]
    
    # 2. Recruiter Node
    res = recruiter_node(state)
    assert "recruiter_feedback" in res
    assert "hiring_verdict" in res["recruiter_feedback"]


@patch("app.services.agent_workflow.call_gemini_json")
def test_agent_nodes_integration(mock_call_gemini):
    # Mocking Gemini call to return specific dictionaries
    mock_call_gemini.side_effect = [
        {"score": 95, "issues": []},  # ATS
        {"hiring_verdict": "Shortlist"}, # Recruiter
        {"writing_score": 90}, # Reviewer
        {"recommended_roles": ["Architect"]}, # Career Advisor
        {"fit_percentage": 92.0} # Consolidator
    ]
    
    with patch("app.services.agent_workflow.LANGGRAPH_AVAILABLE", True), \
         patch("app.services.agent_workflow.settings.GEMINI_API_KEY", "mock_key"):
        result = ResumeAgentWorkflowService.run_agent_workflow("Sample resume", "Target job")
        
        assert result["ats_feedback"]["score"] == 95
        assert result["recruiter_feedback"]["hiring_verdict"] == "Shortlist"
        assert result["reviewer_feedback"]["writing_score"] == 90
        assert result["advisor_feedback"]["recommended_roles"] == ["Architect"]
        assert result["consolidated_report"]["fit_percentage"] == 92.0


def test_agent_analyze_endpoint(client: TestClient, db_session: Session):
    resume_id = uuid.uuid4()
    
    # Check that endpoint returns 200 and records output in DB
    # We mock the workflow service to return a dummy state
    mock_result = {
        "ats_feedback": {"score": 88},
        "recruiter_feedback": {"hiring_verdict": "Shortlist"},
        "reviewer_feedback": {"writing_score": 92},
        "advisor_feedback": {"recommended_roles": ["Architect"]},
        "consolidated_report": {"fit_percentage": 90.0, "summary": "Highly recommended"}
    }
    
    with patch("app.services.agent_workflow.ResumeAgentWorkflowService.run_agent_workflow", return_value=mock_result):
        payload = {
            "resume_id": str(resume_id),
            "job_description": "Lead Cloud architect"
        }
        
        response = client.post("/api/v1/agents/analyze", json=payload)
        
    assert response.status_code == 200
    data = response.json()
    assert data["resume_id"] == str(resume_id)
    assert data["consolidated_report"]["fit_percentage"] == 90.0
    
    # Verify report is written to database
    db_report = db_session.query(AgentReport).filter(
        AgentReport.report_type == "multi_agent_consolidated_report"
    ).first()
    assert db_report is not None
    assert db_report.content["fit_percentage"] == 90.0
