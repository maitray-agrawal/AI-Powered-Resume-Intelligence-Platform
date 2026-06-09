import pytest
from unittest.mock import patch, MagicMock
from app.services.parser_service import ResumeParserService

# Sample resume text for testing parsing rules
SAMPLE_RESUME_TEXT = """
Jane Doe
Software Engineer
Email: janedoe@example.com | Phone: +1 (555) 019-2834 | GitHub: github.com/janedoe

Education
Bachelor of Science in Computer Science
University of Technology, 2018 - 2022

Experience
Senior Software Engineer at TechCorp (2022 - Present)
- Designed and built scalable web applications using Python, FastAPI, and React.
- Deployed services to AWS using Docker and Kubernetes.
- Managed CI/CD pipelines and mentored junior engineers.

Projects
E-commerce Platform Project
- Created a microservices-based shop with Node.js and PostgreSQL.
- Handled transactions securely and integrated search via Elasticsearch.

Skills
Languages: Python, JavaScript, TypeScript, SQL, HTML, CSS, Bash
Tools: Docker, Kubernetes, AWS, Git, Nginx, PostgreSQL
"""

def test_extract_email():
    assert ResumeParserService._extract_email(SAMPLE_RESUME_TEXT) == "janedoe@example.com"
    assert ResumeParserService._extract_email("No email here") == ""

def test_extract_phone():
    # The regex matches formatting characters surrounding numbers
    extracted = ResumeParserService._extract_phone(SAMPLE_RESUME_TEXT)
    assert "555" in extracted
    assert "2834" in extracted
    assert ResumeParserService._extract_phone("Call me at +1-123-456-7890 tomorrow") == "+1-123-456-7890"
    assert ResumeParserService._extract_phone("No phone number") == ""

def test_extract_skills():
    extracted = ResumeParserService._extract_skills(SAMPLE_RESUME_TEXT)
    # Check that expected skills are extracted and formatted nicely
    assert "Python" in extracted
    assert "FastAPI" in extracted
    assert "React" in extracted
    assert "Docker" in extracted
    assert "Kubernetes" in extracted
    assert "AWS" in extracted
    assert "Git" in extracted
    assert "Nginx" in extracted
    assert "PostgreSQL" in extracted
    assert "SQL" in extracted
    # Check that arbitrary non-skills or subsets are not extracted
    assert "Java" not in extracted  # Java is in JavaScript, but should be prevented by word boundary checks
    assert "Go" not in extracted

def test_extract_sections():
    sections = ResumeParserService._extract_sections(SAMPLE_RESUME_TEXT)
    
    assert "Bachelor of Science in Computer Science" in sections["education"]
    assert "University of Technology" in sections["education"]
    
    assert "Senior Software Engineer at TechCorp" in sections["experience"]
    assert "AWS using Docker and Kubernetes" in sections["experience"]
    
    assert "E-commerce Platform Project" in sections["projects"]
    assert "Node.js and PostgreSQL" in sections["projects"]
    
    # Sections shouldn't leak into each other
    assert "Bachelor of Science" not in sections["experience"]
    assert "E-commerce Platform" not in sections["education"]

def test_extract_name_heuristics():
    # Test Name Heuristic 2 (fallback first-line scanner)
    name = ResumeParserService._extract_name(None, SAMPLE_RESUME_TEXT)
    assert name == "Jane Doe"

@patch("app.services.parser_service.ResumeParserService.extract_text")
def test_parse_resume_integration(mock_extract_text):
    mock_extract_text.return_value = SAMPLE_RESUME_TEXT
    
    result = ResumeParserService.parse_resume("dummy_path.pdf")
    
    assert result["name"] == "Jane Doe"
    assert result["email"] == "janedoe@example.com"
    assert "Python" in result["skills"]
    assert "Bachelor of Science in Computer Science" in result["education"]
    assert "Senior Software Engineer" in result["experience"]
    assert "E-commerce Platform" in result["projects"]
