# Database Schema - AI Resume Intelligence Platform

This document details the relational database schema implemented in PostgreSQL.

## Entity Relationship Details

### 1. `users`
Stores recruiter account records for access control.

| Field Name | Type | Key | Description |
|---|---|---|---|
| `id` | UUID | Primary Key | Unique user identifier. |
| `email` | VARCHAR(255) | Unique | Account login email. |
| `hashed_password` | VARCHAR(255) | - | Secure hashed credential. |
| `is_active` | BOOLEAN | - | Active flags indicator. |
| `created_at` | TIMESTAMP | - | Record registration time. |

### 2. `resumes`
Tracks parsed resume file structures and raw data text.

| Field Name | Type | Key | Description |
|---|---|---|---|
| `id` | UUID | Primary Key | Unique document identifier. |
| `filename` | VARCHAR(255) | - | Native file name. |
| `file_path` | VARCHAR(512) | - | Target storage path. |
| `raw_text` | TEXT | - | Extracted full document string. |
| `candidate_name` | VARCHAR(255) | - | Parsed candidate name. |
| `candidate_email`| VARCHAR(255) | - | Parsed candidate email. |
| `parsed_skills` | JSONB | - | Dynamic key-value array of parsed skill fields. |
| `created_at` | TIMESTAMP | - | Indexing record timestamp. |

### 3. `job_descriptions`
Target roles to calculate ATS scores against.

| Field Name | Type | Key | Description |
|---|---|---|---|
| `id` | UUID | Primary Key | Role definition identifier. |
| `title` | VARCHAR(255) | - | Target job title. |
| `raw_text` | TEXT | - | Role descriptions text. |
| `created_at` | TIMESTAMP | - | Insertion date. |

### 4. `ats_matches`
Tracks scoring evaluations logs.

| Field Name | Type | Key | Description |
|---|---|---|---|
| `id` | UUID | Primary Key | Unique evaluation instance. |
| `resume_id` | UUID | Foreign Key | References `resumes.id`. |
| `job_id` | UUID | Foreign Key | References `job_descriptions.id`. |
| `score` | NUMERIC(5,2) | - | Computed percentage score (e.g. 92.50). |
| `feedback` | TEXT | - | AI model evaluation suggestions. |
| `created_at` | TIMESTAMP | - | Scoring evaluation timestamp. |
