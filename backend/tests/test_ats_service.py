from fastapi.testclient import TestClient
from app.services.ats_service import ATSEngineService
from app.schemas.ats import ResumeDataInput


def test_ats_score_calculation_without_keywords():
    # Ideal resume (has all sections, good length, > 10 skills)
    resume = ResumeDataInput(
        name="John Doe",
        email="john@example.com",
        phone="123-456-7890",
        skills=["Python", "FastAPI", "React", "PostgreSQL", "Docker", "Kubernetes", "AWS", "Git", "Nginx", "Linux", "TypeScript"],
        education="B.S. in Computer Science at State University, 2018-2022. Took algorithms and data structures.",
        experience="Software Engineer at InnovateTech from 2022 to Present. Built API backends using FastAPI and React frontends. Managed CI/CD workflows and wrote container configurations.",
        projects="E-Commerce App: Scalable shopping cart microservices system. Open source contributor to several repositories."
    )
    
    result = ATSEngineService.calculate_ats_score(resume=resume)
    
    # 1. Keyword Score (no keywords, count is 11, so score should be 100)
    assert result["keyword_score"] == 100.0
    
    # 2. Section Score (all 4 sections education, experience, projects, skills present -> 100)
    assert result["section_score"] == 100.0
    
    # 3. Length Score
    # Word count: ~13 words (edu) + ~26 words (exp) + ~18 words (proj) = ~57 words.
    # Word count <= 150 should return score 20.0
    assert result["length_score"] == 20.0
    assert "Critically short" in result["suggestions"][0]
    
    # Weight score: (100 * 0.4) + (100 * 0.4) + (20 * 0.2) = 40 + 40 + 4 = 84
    assert result["overall_score"] == 84.0


def test_ats_score_calculation_with_keywords():
    resume = ResumeDataInput(
        name="Jane Doe",
        email="jane@example.com",
        phone="555-555-5555",
        skills=["Python", "FastAPI", "Docker"],
        education="M.S. in CS",
        experience="Developer",
        projects="Code repository"
    )
    
    # Matching keywords: "Python" (yes), "FastAPI" (yes), "PostgreSQL" (no), "Kubernetes" (no)
    # Match rate: 2/4 = 50.0%
    result = ATSEngineService.calculate_ats_score(
        resume=resume,
        job_keywords=["Python", "FastAPI", "PostgreSQL", "Kubernetes"]
    )
    
    assert result["keyword_score"] == 50.0
    assert "Matched 2 out of 4" in result["findings"][0]
    assert "missing job-specific keywords: PostgreSQL, Kubernetes" in result["suggestions"][0]


def test_ats_score_length_tiers():
    # Helper to check length tier scoring
    # Generate long text blocks to verify scoring ranges
    dummy_text_100_words = "word " * 100
    
    # 1. 300 words (education) -> 300 words total
    resume_300 = ResumeDataInput(
        skills=["Python"],
        education=dummy_text_100_words * 3,
        experience="",
        projects=""
    )
    res = ATSEngineService.calculate_ats_score(resume=resume_300)
    assert res["length_score"] == 80.0
    
    # 2. 500 words total -> 100.0 score
    resume_500 = ResumeDataInput(
        skills=["Python"],
        education=dummy_text_100_words * 2,
        experience=dummy_text_100_words * 2,
        projects=dummy_text_100_words
    )
    res = ATSEngineService.calculate_ats_score(resume=resume_500)
    assert res["length_score"] == 100.0


def test_ats_score_endpoint(client: TestClient):
    payload = {
        "resume": {
            "name": "Alex Smith",
            "email": "alex@example.com",
            "phone": "098-765-4321",
            "skills": ["TypeScript", "AWS"],
            "education": "University of Tech",
            "experience": "Lead Developer",
            "projects": "Cloud automation scripts"
        },
        "job_description_keywords": ["TypeScript", "AWS", "Docker"]
    }
    
    response = client.post("/api/v1/ats/score", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert "overall_score" in data
    assert "keyword_score" in data
    assert "section_score" in data
    assert "length_score" in data
    assert "findings" in data
    assert "suggestions" in data
    
    # Match rate: 2/3 = 66.7
    assert data["keyword_score"] == 66.7
