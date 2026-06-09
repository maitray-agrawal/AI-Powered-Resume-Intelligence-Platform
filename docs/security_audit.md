# Security Audit Report

This report evaluates the security posture of the AI-Powered Resume Intelligence Platform, analyzing potential vulnerabilities and providing mitigations.

---

## Executive Summary

The platform follows clean coding structures and leverages modern frameworks (FastAPI, SQLAlchemy, LangChain) which mitigate traditional risks (e.g. SQL Injection). However, there are significant gaps around route authentication and CORS configuration that must be addressed before production hosting.

---

## Vulnerability Findings & Fixes

### 1. Insecure CORS Configuration (Medium Severity)
- **File**: [backend/app/main.py](file:///d:/ATS%20checker/backend/app/main.py#L17)
- **Root Cause**: `allow_origins=["*"]` allows any website to make cross-origin requests to the FastAPI backend API endpoints.
- **Risk**: A malicious site loaded in a user's browser could make requests to the resume platform endpoints.
- **Recommended Fix**: Restrict the origin list in production to only the trusted frontend domains (e.g. Vercel domain):
  ```python
  app.add_middleware(
      CORSMiddleware,
      allow_origins=settings.ALLOWED_ORIGINS,  # load from .env config list
      ...
  )
  ```

### 2. Missing Endpoint Authentication (Critical Severity)
- **File**: [backend/app/api/v1/endpoints/resume.py](file:///d:/ATS%20checker/backend/app/api/v1/endpoints/resume.py) (and others)
- **Root Cause**: API endpoints do not require authorization headers or user authentication tokens. Every request maps to a single hardcoded default database user record.
- **Risk**: Gaining network access to the API allows viewing, adding, or deleting all candidate resumes and evaluations without verification.
- **Recommended Fix**: Integrate OAuth2 password bearer tokens using FastAPI's `Depends` and verify JWT tokens against database users.

### 3. Weak Default Secret Key (High Severity)
- **File**: [backend/app/core/config.py](file:///d:/ATS%20checker/backend/app/core/config.py#L9)
- **Root Cause**: The default `SECRET_KEY` is hardcoded as a fallback string: `"secret_key_for_security_should_be_changed_in_production"`.
- **Risk**: If the fallback is used, attackers can easily forge JWT signatures to impersonate users.
- **Recommended Fix**: Enforce that the application fails to start in production if `SECRET_KEY` is set to the default value, and verify it is injected from the environment.

### 4. File Upload Extension Validation (Low Severity)
- **File**: [backend/app/services/resume.py](file:///d:/ATS%20checker/backend/app/services/resume.py#L37)
- **Root Cause**: The backend validates file extensions by matching string suffixes: `ext not in ['.pdf', '.docx']`.
- **Risk**: Attackers could bypass basic extension checking by manipulating content-type headers or using double extensions (e.g. `exploit.pdf.exe`) on systems with weak file execution logic.
- **Recommended Fix**: Implement magic byte inspection (e.g., using `python-magic`) to verify document structures match standard PDF or ZIP/OfficeOpenXML schemas.

---

## Risk Assessment Matrix

| Vulnerability Domain | Risk Level | Status | Mitigation |
|---|---|---|---|
| **SQL Injection** | Low | Protected | Managed by SQLAlchemy parameterized query compilation |
| **Authentication Deficit** | Critical | Open | Implement JWT verification middleware |
| **Prompt Injection** | Low | Mitigated | Strict instruction parameters set in system prompts |
| **Secrets Exposure** | Low | Mitigated | Credentials ignored from Git via `.gitignore` policies |
| **CORS Wildcard** | Medium | Open | Lock down to specific domains |
