import pytest
import numpy as np
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from app.services.jd_matcher import JDMatcherService


def test_cosine_similarity_edge_cases():
    from app.services.jd_matcher import calculate_cosine_similarity
    
    # Standard math validation
    v1 = np.array([1.0, 0.0, 0.0])
    v2 = np.array([1.0, 0.0, 0.0])
    assert calculate_cosine_similarity(v1, v2) == 1.0
    
    v3 = np.array([0.0, 1.0, 0.0])
    assert calculate_cosine_similarity(v1, v3) == 0.0
    
    # Zero vector safety
    v_zero = np.array([0.0, 0.0, 0.0])
    assert calculate_cosine_similarity(v1, v_zero) == 0.0


@patch("app.services.jd_matcher.get_jd_model")
def test_jd_matcher_service_calculation(mock_get_model):
    # Setup mock transformer
    mock_transformer = MagicMock()
    mock_get_model.return_value = mock_transformer

    # We mock encode to return specific vectors
    # Let's map texts to embeddings
    # 1. Full texts match perfectly: return identical vectors
    # 2. Skills match partially: return vectors with 0.5 cosine similarity
    def mock_encode(text):
        if "Perfect Resume" in text or "Perfect Job" in text:
            return np.array([1.0, 0.0])
        elif text == "Python, SQL":
            # skills string
            return np.array([1.0, 0.0])
        elif text == "Python, SQL, React, AWS":
            # jd skills string (45-degree angle -> 0.707 similarity)
            return np.array([1.0, 1.0])
        return np.array([0.0, 1.0])

    mock_transformer.encode.side_effect = mock_encode

    result = JDMatcherService.calculate_semantic_match(
        resume_text="Perfect Resume text content",
        resume_skills=["Python", "SQL"],
        job_description_text="Perfect Job Description content",
        job_description_skills=["Python", "SQL", "React", "AWS"]
    )

    # resume_similarity: perfect match -> 1.0
    assert result["resume_similarity"] == 1.0
    # skill_similarity: cos_sim([1.0, 0.0], [1.0, 1.0]) = 1.0 / sqrt(2) = 0.7071
    assert abs(result["skill_similarity"] - 0.7071) < 0.001
    
    # overall match percentage: (1.0 * 0.5 + 0.7071 * 0.5) * 100 = 85.36%
    assert abs(result["match_percentage"] - 85.36) < 0.05


@patch("app.services.jd_matcher.get_jd_model")
def test_jd_matcher_endpoint(mock_get_model, client: TestClient):
    # Setup mock transformer
    mock_transformer = MagicMock()
    mock_get_model.return_value = mock_transformer
    mock_transformer.encode.return_value = np.array([1.0, 0.0])

    payload = {
        "resume_text": "Experienced software architect",
        "resume_skills": ["Python", "AWS"],
        "job_description_text": "We need a cloud engineer",
        "job_description_skills": ["Python", "AWS"]
    }

    response = client.post("/api/v1/jd-matcher/match", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert "resume_similarity" in data
    assert "skill_similarity" in data
    assert "match_percentage" in data
    
    # Since mock returns identical vectors for all calls, similarities should be 1.0 and match percentage 100.0
    assert data["resume_similarity"] == 1.0
    assert data["skill_similarity"] == 1.0
    assert data["match_percentage"] == 100.0
