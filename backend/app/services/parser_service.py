import os
import re
import uuid
import spacy
from typing import Dict, Any, List
from docx import Document
from spacy.cli import download

# Lazy loading of spaCy model
nlp = None

def get_spacy_nlp():
    global nlp
    if nlp is not None:
        return nlp
    try:
        nlp = spacy.load("en_core_web_sm")
    except OSError:
        try:
            download("en_core_web_sm")
            nlp = spacy.load("en_core_web_sm")
        except Exception as e:
            print(f"Warning: Failed to load/download spaCy model en_core_web_sm: {e}")
            nlp = None
    return nlp


# A comprehensive dictionary of common tech skills mapping search keywords to display names
SKILLS_DICT = {
    "python": "Python",
    "javascript": "JavaScript",
    "typescript": "TypeScript",
    "java": "Java",
    "c++": "C++",
    "c#": "C#",
    "go": "Go",
    "rust": "Rust",
    "ruby": "Ruby",
    "php": "PHP",
    "swift": "Swift",
    "kotlin": "Kotlin",
    "scala": "Scala",
    "r": "R",
    "sql": "SQL",
    "html": "HTML",
    "css": "CSS",
    "bash": "Bash",
    "react": "React",
    "vue": "Vue",
    "angular": "Angular",
    "svelte": "Svelte",
    "next.js": "Next.js",
    "nextjs": "Next.js",
    "nuxt": "Nuxt.js",
    "django": "Django",
    "flask": "Flask",
    "fastapi": "FastAPI",
    "express": "Express",
    "spring boot": "Spring Boot",
    "laravel": "Laravel",
    "rails": "Ruby on Rails",
    "pytorch": "PyTorch",
    "tensorflow": "TensorFlow",
    "pandas": "Pandas",
    "numpy": "NumPy",
    "scikit-learn": "scikit-learn",
    "keras": "Keras",
    "nltk": "NLTK",
    "spacy": "spaCy",
    "postgresql": "PostgreSQL",
    "postgres": "PostgreSQL",
    "mysql": "MySQL",
    "mongodb": "MongoDB",
    "redis": "Redis",
    "sqlite": "SQLite",
    "cassandra": "Cassandra",
    "oracle": "Oracle",
    "sql server": "SQL Server",
    "mariadb": "MariaDB",
    "dynamodb": "DynamoDB",
    "elasticsearch": "Elasticsearch",
    "docker": "Docker",
    "kubernetes": "Kubernetes",
    "aws": "AWS",
    "gcp": "GCP",
    "azure": "Azure",
    "git": "Git",
    "github": "GitHub",
    "gitlab": "GitLab",
    "jenkins": "Jenkins",
    "circleci": "CircleCI",
    "github actions": "GitHub Actions",
    "nginx": "Nginx",
    "apache": "Apache",
    "linux": "Linux",
    "unix": "Unix",
    "jira": "Jira",
    "confluence": "Confluence",
    "terraform": "Terraform",
    "ansible": "Ansible",
    "helm": "Helm",
    "agile": "Agile",
    "scrum": "Scrum",
    "ci/cd": "CI/CD",
    "microservices": "Microservices",
    "rest api": "REST API",
    "graphql": "GraphQL",
    "machine learning": "Machine Learning",
    "deep learning": "Deep Learning",
    "nlp": "NLP",
    "natural language processing": "Natural Language Processing",
    "computer vision": "Computer Vision",
    "data science": "Data Science",
    "data analysis": "Data Analysis",
    "web development": "Web Development",
    "software engineering": "Software Engineering"
}


class ResumeParserService:
    @staticmethod
    def extract_text_from_pdf_pymupdf(file_path: str) -> str:
        """Extracts text from PDF using PyMuPDF (fitz)"""
        import fitz
        text = ""
        doc = fitz.open(file_path)
        for page in doc:
            text += page.get_text() or ""
        return text

    @staticmethod
    def extract_text_from_pdf_pdfplumber(file_path: str) -> str:
        """Extracts text from PDF using pdfplumber"""
        import pdfplumber
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
        return text

    @classmethod
    def extract_text_from_pdf(cls, file_path: str) -> str:
        """Extracts text from PDF using PyMuPDF, with pdfplumber as fallback"""
        try:
            return cls.extract_text_from_pdf_pymupdf(file_path)
        except Exception as e:
            print(f"PyMuPDF failed, falling back to pdfplumber: {e}")
            try:
                return cls.extract_text_from_pdf_pdfplumber(file_path)
            except Exception as e_inner:
                raise ValueError(f"Failed to parse PDF using PyMuPDF and pdfplumber: {e_inner}")

    @staticmethod
    def extract_text_from_docx(file_path: str) -> str:
        """Extracts text from Word documents using python-docx"""
        doc = Document(file_path)
        text = []
        for para in doc.paragraphs:
            text.append(para.text)
        return "\n".join(text)

    @classmethod
    def extract_text(cls, file_path: str) -> str:
        """Main raw text extraction entrypoint supporting PDF and DOCX"""
        _, ext = os.path.splitext(file_path)
        ext = ext.lower()
        if ext == '.pdf':
            return cls.extract_text_from_pdf(file_path)
        elif ext in ['.docx', '.doc']:
            return cls.extract_text_from_docx(file_path)
        else:
            raise ValueError(f"Unsupported file format '{ext}'")

    @classmethod
    def parse_resume(cls, file_path: str) -> Dict[str, Any]:
        """Parses a resume file and returns structured JSON details"""
        raw_text = cls.extract_text(file_path)
        
        # Load spaCy nlp model
        spacy_nlp = get_spacy_nlp()
        doc = spacy_nlp(raw_text) if spacy_nlp else None
        
        # Extract individual structured fields
        name = cls._extract_name(doc, raw_text)
        email = cls._extract_email(raw_text)
        phone = cls._extract_phone(raw_text)
        skills = cls._extract_skills(raw_text)
        
        sections = cls._extract_sections(raw_text)
        
        return {
            "name": name,
            "email": email,
            "phone": phone,
            "skills": skills,
            "education": sections["education"],
            "projects": sections["projects"],
            "experience": sections["experience"]
        }

    @classmethod
    def _extract_name(cls, doc, text: str) -> str:
        """Extracts the candidate's name using spaCy NER and first line heuristics"""
        # Heuristic 1: Scan first few PERSON entities from spaCy doc
        if doc:
            for ent in doc.ents:
                if ent.label_ == "PERSON":
                    candidate = ent.text.strip().replace("\n", " ")
                    # Check if candidate name length and format look plausible (2-4 words, alphabet-only mostly)
                    words = [w for w in candidate.split() if w.isalpha()]
                    if 1 < len(words) <= 4 and len(candidate) < 35:
                        candidate_lower = candidate.lower()
                        bad_keywords = [
                            "resume", "cv", "education", "experience", "projects", "skills",
                            "engineer", "developer", "designer", "manager", "analyst", "consultant",
                            "intern", "coordinator", "officer", "director", "lead", "specialist",
                            "architect", "programmer", "administrator", "scientist", "curriculum", "vitae"
                        ]
                        if not any(k in candidate_lower for k in bad_keywords):
                            return candidate


        # Heuristic 2: Fallback to scanning the first 4 non-empty lines
        lines = [line.strip() for line in text.split("\n") if line.strip()]
        for line in lines[:4]:
            # Clean and strip bullets or marks
            cleaned = re.sub(r'^[#\-\*\s•\d\.\)]+', '', line).strip()
            # If it's a short line of alphabetic words (typically a name on first line)
            words = cleaned.split()
            if 1 < len(words) <= 4 and all(w.isalpha() or (w.endswith('.') and len(w) <= 2) for w in words) and len(cleaned) < 35:
                if cleaned.lower() not in ["resume", "cv", "curriculum vitae", "education", "experience", "skills"]:
                    return cleaned

        return "Unknown"

    @classmethod
    def _extract_email(cls, text: str) -> str:
        """Extracts first valid email address found in the text"""
        email_regex = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')
        matches = email_regex.findall(text)
        return matches[0] if matches else ""

    @classmethod
    def _extract_phone(cls, text: str) -> str:
        """Extracts first valid phone number matching standard patterns"""
        phone_regex = re.compile(
            r'(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        )
        matches = phone_regex.findall(text)
        return matches[0] if matches else ""

    @classmethod
    def _extract_skills(cls, text: str) -> List[str]:
        """Extracts skills matching a curated list of technical and soft skills"""
        matched_skills = set()
        for skill_key, skill_display in SKILLS_DICT.items():
            if skill_key.endswith('+') or skill_key.endswith('#'):
                pattern = rf"\b{re.escape(skill_key)}(?!\w)"
            else:
                pattern = rf"\b{re.escape(skill_key)}\b"
                
            if re.search(pattern, text, re.IGNORECASE):
                matched_skills.add(skill_display)
        return sorted(list(matched_skills))

    @classmethod
    def _extract_sections(cls, text: str) -> Dict[str, str]:
        """Extracts specific sections (education, projects, experience) based on header keywords"""
        headers_config = {
            "education": [r"education", r"academic\s+background", r"academic\s+profile", r"qualifications?"],
            "experience": [r"work\s+experience", r"professional\s+experience", r"experience", r"employment\s+history", r"work\s+history"],
            "projects": [r"projects", r"personal\s+projects", r"academic\s+projects", r"key\s+projects"],
            "skills_section": [r"skills", r"technical\s+skills", r"core\s+competencies", r"key\s+skills"]
        }
        
        lines = text.split('\n')
        section_bounds = []
        
        for idx, line in enumerate(lines):
            clean_line = line.strip().lower()
            if len(clean_line) > 40 or not clean_line:
                continue
            
            # Remove markdown, numbers, bullets, or trailing colons
            clean_line_stripped = re.sub(r'^[#\-\*\s•\d\.\)]+', '', clean_line).strip()
            clean_line_stripped = re.sub(r'[:\s]+$', '', clean_line_stripped).strip()
            
            for sec_name, patterns in headers_config.items():
                matched = False
                for pat in patterns:
                    if re.match(f"^{pat}$", clean_line_stripped):
                        section_bounds.append((idx, sec_name, line))
                        matched = True
                        break
                if matched:
                    break

        # Sort and deduplicate sections (keep the first match of each section type)
        section_bounds.sort(key=lambda x: x[0])
        seen_sections = set()
        deduped_bounds = []
        for bound in section_bounds:
            sec_name = bound[1]
            if sec_name not in seen_sections:
                seen_sections.add(sec_name)
                deduped_bounds.append(bound)
                
        deduped_bounds.sort(key=lambda x: x[0])
        
        extracted_sections = {
            "education": "",
            "experience": "",
            "projects": ""
        }
        
        for i, bound in enumerate(deduped_bounds):
            start_line_idx = bound[0] + 1
            sec_name = bound[1]
            
            end_line_idx = len(lines)
            if i + 1 < len(deduped_bounds):
                end_line_idx = deduped_bounds[i+1][0]
                
            section_text = "\n".join(lines[start_line_idx:end_line_idx]).strip()
            if sec_name in extracted_sections:
                extracted_sections[sec_name] = section_text
                
        return extracted_sections
