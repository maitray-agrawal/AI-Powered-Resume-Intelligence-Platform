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


def test_upload_resume_dummy_pdf(client: TestClient):
    # Basic PDF structure bytes
    pdf_content = b"%PDF-1.4\n1 0 obj\n<<\n/Type /Catalog\n>>\nendobj\ntrailer\n<<\n/Root 1 0 R\n>>\n%%EOF"
    with patch("app.services.resume.ResumeParser.extract_text", return_value="Dummy extracted resume text content"):
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

