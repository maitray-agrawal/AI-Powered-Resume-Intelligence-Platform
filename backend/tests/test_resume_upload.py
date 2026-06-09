import io
from fastapi.testclient import TestClient


def test_upload_resume_unsupported_format(client: TestClient):
    response = client.post(
        "/api/v1/resume/upload",
        files={"file": ("test.txt", io.BytesIO(b"unsupported content"), "text/plain")}
    )
    assert response.status_code == 400
    assert "Unsupported file format" in response.json()["detail"]


from unittest.mock import patch


@patch("app.services.parser_service.ResumeParserService.parse_resume")
@patch("app.services.parser_service.ResumeParserService.extract_text")
def test_upload_resume_dummy_pdf(mock_extract_text, mock_parse_resume, client: TestClient):
    mock_extract_text.return_value = "Dummy extracted resume text content"
    mock_parse_resume.return_value = {
        "name": "Jane Doe",
        "email": "janedoe@example.com",
        "phone": "+1 (555) 019-2834",
        "skills": ["Python", "FastAPI"],
        "education": "BS in CS",
        "projects": "Project A",
        "experience": "Senior Dev"
    }
    # Basic PDF structure bytes
    pdf_content = b"%PDF-1.4\n1 0 obj\n<<\n/Type /Catalog\n>>\nendobj\ntrailer\n<<\n/Root 1 0 R\n>>\n%%EOF"
    response = client.post(
        "/api/v1/resume/upload",
        files={"file": ("test_resume.pdf", io.BytesIO(pdf_content), "application/pdf")}
    )
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["title"] == "test_resume.pdf"
    assert "latest_version" in data
    assert data["latest_version"]["version_number"] == 1
    assert data["latest_version"]["file_name"] == "test_resume.pdf"

