import uuid
from datetime import datetime, timezone, timedelta
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models import User, Resume, ResumeVersion, JobDescription, ATSReport, MatchReport, AgentReport


def test_get_dashboard_analytics_empty_db(client: TestClient):
    """Verify both POST and GET endpoints return fallback seed data when the database is empty."""
    for method in ["get", "post"]:
        if method == "get":
            response = client.get("/api/v1/analytics/dashboard")
        else:
            response = client.post("/api/v1/analytics/dashboard")
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify response structure
        assert "ats_score_history" in data
        assert "jd_match_history" in data
        assert "skill_gaps" in data
        assert "agent_scores" in data
        
        # Verify fallback data is populated
        assert len(data["ats_score_history"]) >= 5
        assert data["ats_score_history"][0]["score"] == 70.0
        
        assert len(data["jd_match_history"]) >= 4
        assert data["jd_match_history"][0]["role"] == "Frontend Architect"
        
        assert len(data["skill_gaps"]) >= 5
        # Docker should be first since it has highest frequency (8)
        assert data["skill_gaps"][0]["skill"] == "Docker"
        
        assert len(data["agent_scores"]) >= 4
        assert any(item["agent"] == "ATS Expert" and item["score"] == 85.0 for item in data["agent_scores"])
        
        # Verify items have required fields
        for item in data["ats_score_history"]:
            assert "date" in item
            assert "score" in item
        
        for item in data["jd_match_history"]:
            assert "role" in item
            assert "score" in item
        
        for item in data["skill_gaps"]:
            assert "skill" in item
            assert "frequency" in item
        
        for item in data["agent_scores"]:
            assert "agent" in item
            assert "score" in item


def test_get_dashboard_analytics_with_data(client: TestClient, db_session: Session):
    """
    Test analytics with seeded database records.
    Uses dependency injection to share the test db_session with the FastAPI client.
    """
    from app.core.database import get_db
    
    def override_get_db():
        yield db_session
        
    client.app.dependency_overrides[get_db] = override_get_db
    
    try:
        # Setup identifiers
        user_id = uuid.uuid4()
        resume_id = uuid.uuid4()
        resume_version_id = uuid.uuid4()
        jd_id = uuid.uuid4()
        
        # 1. Create a dummy user
        user = User(
            id=user_id,
            email="test_analytics_user@example.com",
            hashed_password="hashed_password_placeholder",
            is_active=True
        )
        db_session.add(user)
        db_session.commit()
        
        # 2. Create a Resume
        resume = Resume(
            id=resume_id,
            user_id=user_id,
            title="Software Engineer Resume"
        )
        db_session.add(resume)
        db_session.commit()
        
        # 3. Create a Resume Version
        resume_version = ResumeVersion(
            id=resume_version_id,
            resume_id=resume_id,
            version_number=1,
            file_name="resume.pdf",
            file_path="/path/to/resume.pdf",
            raw_text="Experienced Software Engineer with Python and AWS",
            structured_data={}
        )
        db_session.add(resume_version)
        db_session.commit()
        
        # 4. Create ATS Reports (2 records — still triggers fallback merge since < 3)
        now = datetime.now(timezone.utc)
        ats_report_1 = ATSReport(
            id=uuid.uuid4(),
            resume_version_id=resume_version_id,
            score=85.0,
            findings={},
            suggestions={},
            created_at=now - timedelta(days=2)
        )
        ats_report_2 = ATSReport(
            id=uuid.uuid4(),
            resume_version_id=resume_version_id,
            score=92.5,
            findings={},
            suggestions={},
            created_at=now
        )
        db_session.add(ats_report_1)
        db_session.add(ats_report_2)
        db_session.commit()
        
        # 5. Create Job Description
        jd = JobDescription(
            id=jd_id,
            user_id=user_id,
            title="Senior Python Specialist",
            company="Tech Corp",
            description_text="Looking for a Python specialist",
            requirements={}
        )
        db_session.add(jd)
        db_session.commit()
        
        # 6. Create Match Report with 2 missing skills: "FastAPI", "Docker"
        match_report = MatchReport(
            id=uuid.uuid4(),
            resume_version_id=resume_version_id,
            job_description_id=jd_id,
            score=88.0,
            skills_matched=["Python", "SQL"],
            skills_missing=["FastAPI", "Docker"],
            feedback="Great resume",
            created_at=now
        )
        db_session.add(match_report)
        
        # 7. Create Agent Report with all four feedback types
        agent_report = AgentReport(
            id=uuid.uuid4(),
            user_id=user_id,
            report_type="multi_agent_consolidated_report",
            content={
                "ats_feedback": {"score": 90.0},
                "recruiter_feedback": {"fit_rating": 4},   # 4 * 20 = 80.0
                "reviewer_feedback": {"writing_score": 95.0},
                "consolidated_report": {"fit_percentage": 85.0}
            },
            created_at=now
        )
        db_session.add(agent_report)
        db_session.commit()
        
        # ---- Make the API call ----
        response = client.get("/api/v1/analytics/dashboard")
        assert response.status_code == 200
        data = response.json()
        
        # ---- ATS Score History ----
        # 2 DB records < 3 threshold → defaults (5) + DB records (2) = 7
        ats_history = data["ats_score_history"]
        assert len(ats_history) >= 7, f"Expected >= 7 ATS records, got {len(ats_history)}"
        # DB records appended at end in chronological order
        scores = [item["score"] for item in ats_history]
        assert 85.0 in scores, "Expected ats_report_1 score (85.0) in history"
        assert 92.5 in scores, "Expected ats_report_2 score (92.5) in history"
        
        # ---- JD Match History ----
        # Should contain our new JD title
        jd_roles = [item["role"] for item in data["jd_match_history"]]
        assert "Senior Python Specialist" in jd_roles, f"Expected 'Senior Python Specialist' in {jd_roles}"
        match_entry = next(i for i in data["jd_match_history"] if i["role"] == "Senior Python Specialist")
        assert match_entry["score"] == 88.0
        
        # ---- Skill Gaps ----
        # DB returns 2 unique skills: FastAPI (freq=1), Docker (freq=1).
        # After merge with 5 defaults, sorted desc: AWS(6), K8s(5), TS(4), PG(3), FastAPI(1), Docker(1)
        # top-5 → Docker gets cut off (rank 6). FastAPI makes it in at rank 5.
        skill_names = [item["skill"] for item in data["skill_gaps"]]
        # Confirm FastAPI is in the top-5 list (it's the unique skill from DB)
        assert "FastAPI" in skill_names, f"Expected 'FastAPI' in skill gaps: {skill_names}"
        # Confirm default seeds are present (e.g., AWS Solutions ranked #1 in merge)
        assert "AWS Solutions" in skill_names, f"Expected 'AWS Solutions' in skill gaps: {skill_names}"
        
        # ---- Agent Scores ----
        # All 4 agents should have real DB-sourced scores (no defaults needed)
        agent_score_map = {item["agent"]: item["score"] for item in data["agent_scores"]}
        assert agent_score_map.get("ATS Expert") == 90.0, f"ATS Expert: {agent_score_map}"
        assert agent_score_map.get("Recruiter") == 80.0, f"Recruiter: {agent_score_map}"
        assert agent_score_map.get("Resume Reviewer") == 95.0, f"Resume Reviewer: {agent_score_map}"
        assert agent_score_map.get("Career Advisor") == 85.0, f"Career Advisor: {agent_score_map}"
        
    finally:
        # Always restore original dependency overrides
        if get_db in client.app.dependency_overrides:
            del client.app.dependency_overrides[get_db]
