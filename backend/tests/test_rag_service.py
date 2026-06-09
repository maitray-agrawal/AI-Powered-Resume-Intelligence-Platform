import pytest
import uuid
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from app.services.rag_service import ResumeRAGService


def test_rag_service_mock_fallbacks_when_offline():
    # Verify that in offline mode (no API key / vector store), the service falls back to default responses
    resume_id = uuid.uuid4()
    resume_text = "Sample resume content containing education, skills, and work experience."
    
    with patch("app.services.rag_service.ResumeRAGService.get_vectorstore", return_value=None):
        # Ingestion fallback maps chunks based on word count
        num_chunks = ResumeRAGService.ingest_resume(resume_id, resume_text)
        assert num_chunks == 1
        
        # Chat fallback matches keywords
        ans, sources = ResumeRAGService.chat_with_resume(resume_id, "What are the skills?")
        assert "skills include Python, JavaScript, React" in ans
        assert len(sources) > 0


@patch("app.services.rag_service.ResumeRAGService.get_vectorstore")
def test_rag_ingest_service_success(mock_get_store):
    mock_store = MagicMock()
    mock_get_store.return_value = mock_store
    
    resume_id = uuid.uuid4()
    resume_text = "Word " * 600  # generates text long enough to split into multiple chunks
    
    num_chunks = ResumeRAGService.ingest_resume(resume_id, resume_text)
    
    assert num_chunks > 1
    mock_store.add_documents.assert_called_once()


@patch("app.services.rag_service.ResumeRAGService.get_vectorstore")
@patch("app.services.rag_service.ChatGoogleGenerativeAI")
def test_rag_chat_service_success(mock_chat_llm, mock_get_store):
    # Mock Chroma vectorstore search
    mock_store = MagicMock()
    mock_get_store.return_value = mock_store
    
    mock_doc = MagicMock()
    mock_doc.page_content = "Relevant resume chunk containing FastAPI experience."
    mock_store.similarity_search.return_value = [mock_doc]
    
    # Mock LLM Q&A
    mock_llm = MagicMock()
    mock_chat_llm.return_value = mock_llm
    mock_response = MagicMock()
    mock_response.content = "Answer generated based on context."
    mock_llm.invoke.return_value = mock_response

    resume_id = uuid.uuid4()
    ans, sources = ResumeRAGService.chat_with_resume(resume_id, "FastAPI details?")
    
    assert ans == "Answer generated based on context."
    assert len(sources) == 1
    assert "FastAPI experience" in sources[0]
    mock_store.similarity_search.assert_called_once()
    mock_llm.invoke.assert_called_once()


def test_rag_ingest_endpoint(client: TestClient):
    resume_id = str(uuid.uuid4())
    payload = {
        "resume_id": resume_id,
        "resume_text": "Jane Doe. Web Developer. Experience building React applications."
    }
    
    # Mock get_vectorstore to force mock mode in endpoint
    with patch("app.services.rag_service.ResumeRAGService.get_vectorstore", return_value=None):
        response = client.post("/api/v1/rag/ingest", json=payload)
        
    assert response.status_code == 201
    data = response.json()
    assert data["success"] is True
    assert data["num_chunks"] > 0


def test_rag_chat_endpoint(client: TestClient):
    resume_id = str(uuid.uuid4())
    payload = {
        "resume_id": resume_id,
        "query": "Tell me about education."
    }
    
    with patch("app.services.rag_service.ResumeRAGService.get_vectorstore", return_value=None):
        response = client.post("/api/v1/rag/chat", json=payload)
        
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert "sources" in data
    assert "Bachelor of Science" in data["answer"]
