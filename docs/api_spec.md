# API Specifications - AI Resume Intelligence Platform

The platform exposes RESTful endpoints under `/api/v1`.

## Endpoints

### 1. Resume Operations

#### Upload Resume
- **Path**: `POST /api/v1/resumes/upload`
- **Content-Type**: `multipart/form-data`
- **Request**: File payload (PDF, DOCX)
- **Response**: `201 Created`
  ```json
  {
    "id": "uuid-string-here",
    "filename": "resume.pdf",
    "status": "processed",
    "extracted_metadata": {
      "name": "Jane Doe",
      "email": "jane@example.com"
    }
  }
  ```

#### List Resumes
- **Path**: `GET /api/v1/resumes`
- **Response**: `200 OK` (Array of resume metadata records)

#### Delete Resume
- **Path**: `DELETE /api/v1/resumes/{id}`
- **Response**: `200 OK` (Confirms deletion from Postgres and ChromaDB)

---

### 2. Search & Intelligence

#### Semantic Search Query
- **Path**: `POST /api/v1/search/query`
- **Body**:
  ```json
  {
    "query": "React frontend developer with python experience",
    "limit": 10
  }
  ```
- **Response**: `200 OK` (Array of candidate matches ranked by similarity score)

#### ATS Match Score
- **Path**: `POST /api/v1/search/match`
- **Body**:
  ```json
  {
    "resume_id": "uuid-string-here",
    "job_description": "Job requirements content..."
  }
  ```
- **Response**: `200 OK`
  ```json
  {
    "score": 85.5,
    "analysis": {
      "matching_skills": ["React", "Python"],
      "missing_skills": ["PostgreSQL"],
      "feedback": "Add database design highlights."
    }
  }
  ```
