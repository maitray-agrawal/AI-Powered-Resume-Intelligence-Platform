import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from app.services.llm_service import GeminiLLMService


def test_llm_service_mock_fallbacks_when_no_client():
    # If no Gemini Client is available, it should fall back to high-quality mock responses
    with patch("app.services.llm_service.GeminiLLMService.get_client", return_value=None):
        improvements = GeminiLLMService.resume_improvement("My Resume Text")
        assert len(improvements) == 3
        assert "Quantify achievements" in improvements[0]

        rewrites = GeminiLLMService.resume_rewrite("Resume content", "Frontend Engineer", ["experience"])
        assert "experience" in rewrites
        assert "Frontend Engineer" in rewrites["experience"]

        prep = GeminiLLMService.interview_questions("Resume content", "Job description")
        assert len(prep) == 2
        assert "question" in prep[0]

        letter = GeminiLLMService.cover_letter("Resume content", "Job description")
        assert "Dear Hiring Manager" in letter


@patch("app.services.llm_service.GeminiLLMService.get_client")
def test_llm_service_calls_gemini_api(mock_get_client):
    mock_client = MagicMock()
    mock_get_client.return_value = mock_client
    
    mock_response = MagicMock()
    mock_response.text = '["Improve design patterns.", "Add unit tests."]'
    mock_client.models.generate_content.return_value = mock_response

    improvements = GeminiLLMService.resume_improvement("Experienced developer", "Need software engineer")
    
    assert len(improvements) == 2
    assert improvements[0] == "Improve design patterns."
    assert improvements[1] == "Add unit tests."
    mock_client.models.generate_content.assert_called_once()


def test_llm_improvement_endpoint(client: TestClient):
    payload = {
        "resume_text": "Experienced Python Backend developer",
        "job_description": "We need a FastAPI Backend Engineer"
    }
    
    # Force mock mode
    with patch("app.services.llm_service.GeminiLLMService.get_client", return_value=None):
        response = client.post("/api/v1/llm/improvement", json=payload)
        
    assert response.status_code == 200
    data = response.json()
    assert "improvements" in data
    assert len(data["improvements"]) > 0


def test_llm_rewrite_endpoint(client: TestClient):
    payload = {
        "resume_text": "Developer at XYZ",
        "target_role": "Senior Developer",
        "sections_to_rewrite": ["experience", "summary"]
    }
    
    with patch("app.services.llm_service.GeminiLLMService.get_client", return_value=None):
        response = client.post("/api/v1/llm/rewrite", json=payload)
        
    assert response.status_code == 200
    data = response.json()
    assert "rewritten_sections" in data
    assert "experience" in data["rewritten_sections"]
    assert "summary" in data["rewritten_sections"]


def test_llm_interview_questions_endpoint(client: TestClient):
    payload = {
        "resume_text": "Full stack dev",
        "job_description": "React developer"
    }
    
    with patch("app.services.llm_service.GeminiLLMService.get_client", return_value=None):
        response = client.post("/api/v1/llm/interview-questions", json=payload)
        
    assert response.status_code == 200
    data = response.json()
    assert "questions" in data
    assert len(data["questions"]) > 0
    assert "question" in data["questions"][0]
    assert "rationale" in data["questions"][0]
    assert "suggested_approach" in data["questions"][0]


def test_llm_cover_letter_endpoint(client: TestClient):
    payload = {
        "resume_text": "Architect",
        "job_description": "Principal Architect"
    }
    
    with patch("app.services.llm_service.GeminiLLMService.get_client", return_value=None):
        response = client.post("/api/v1/llm/cover-letter", json=payload)
        
    assert response.status_code == 200
    data = response.json()
    assert "cover_letter" in data
    assert "Dear Hiring Manager" in data["cover_letter"]
