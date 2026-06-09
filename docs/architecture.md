# System Architecture & Technical Specification

This document provides a deep dive into the system design, data flows, and architectural layers of the AI-Powered Resume Intelligence Platform.

---

## High-Level Architecture Diagram

```mermaid
graph TD
    Client[React + Vite Frontend] <-->|JSON / REST API| Server[FastAPI Backend]
    
    subgraph Storage
        Server <-->|SQL / PostgreSQL| DB[(PostgreSQL Database)]
        Server <-->|gRPC / HTTP| VectorDB[(ChromaDB Vector Store)]
    end
    
    subgraph AI Pipeline
        Server <-->|Gemini API| Gemini[Google Gemini LLM]
        Server -->|Local Inference| ST[Sentence-Transformers]
        Server -->|Local Inference| Spacy[spaCy NER Model]
    end
    
    subgraph Telemetry
        Server -->|Experiment Tracking| MLflow[MLflow Server]
    end
```

---

## Architectural Layers

### 1. Frontend Client
- **Core Stack**: React 18, TypeScript, TailwindCSS.
- **Routing**: Single Page Application (SPA) routing via `react-router-dom`.
- **Charts**: Recharts (`AreaChart`, `BarChart`, `RadarChart`) for analytics visualization.
- **API Client**: Axios-based client utilizing environmental base URLs and local mocks fallback.

### 2. FastAPI Backend Application
- **Routing**: Modular FastAPI routing grouped by feature domains (`/resume`, `/ats`, `/jd-matcher`, `/llm`, `/rag`, `/agents`, `/analytics`).
- **Database Engine**: SQLAlchemy ORM with connection pooling, transactional management, and Alembic schema versioning.
- **AI Service Orchestration**: Encapsulates document extraction, semantic indexing, LangGraph workflows, and Gemini LLM prompts in decoupled service modules.

### 3. Storage Layer
- **Relational Data**: PostgreSQL stores persistent structural schemas (users, resumes, versions, reports, chat sessions).
- **Vector Data**: ChromaDB index stores high-dimensional dense vector embeddings of resume segments for semantically filtered contextual queries.

### 4. LLM & Inference Layer
- **Generation Model**: `gemini-2.5-flash` for multi-agent reasoning, resume rewrite generation, interview Q&A, and cover letters.
- **Embedding Model**: `models/embedding-001` for RAG document chunking vector generation.
- **Local Embeddings**: `all-MiniLM-L6-v2` via `sentence-transformers` for calculating cosine similarities without external API delays.
- **Local NER**: `en_core_web_sm` via `spaCy` for high-throughput heuristic metadata extraction.

---

## Data Flow Diagram

```mermaid
sequenceDiagram
    autonumber
    actor User as User Browser
    participant API as FastAPI Backend
    participant DB as PostgreSQL
    participant RAG as ChromaDB
    participant AI as Gemini API

    User->>API: Upload PDF/DOCX Resume
    API->>API: Extract Raw Text & Metadata
    API->>DB: Save Resume & Version metadata
    API->>RAG: Chunk, Embed & Index Chunks
    RAG-->>API: Ingestion Ack (num chunks)
    API-->>User: Upload Success & Version ID
    
    User->>API: Request RAG Chat (Query + Version ID)
    API->>RAG: Retrieve Top K Chunks (filtered by resume_id)
    RAG-->>API: Return Source Context
    API->>AI: Send Prompt (Context + Query)
    AI-->>API: Return Answer Text
    API-->>User: Send Answer & Source Chunks
```

---

## RAG Pipeline Flow

```mermaid
flowchart TD
    DocInput[Raw Resume File] --> Parse[Text Extraction]
    Parse --> Split[Recursive Character Text Splitter]
    Split --> Chunks[Text Chunks: size 400, overlap 40]
    
    subgraph Indexing
        Chunks --> Embed[Google GenerativeAI Embeddings]
        Embed --> Chroma[ChromaDB Collection]
    end
    
    Query[User Chat Query] --> Match[Vector Similarity Match]
    Chroma -->|Metadata Filter: resume_id| Match
    Match --> Context[Retrieve Context Documents]
    Context --> Prompt[Build Contextual Prompt]
    Query --> Prompt
    Prompt --> Gemini[Gemini 2.5 Flash]
    Gemini --> Answer[Generated Contextual Answer]
```

---

## LangGraph Multi-Agent Workflow

The agentic pipeline is organized as a sequential directed graph (`StateGraph`) where independent agents evaluate candidate details and transition to the next evaluator, culminating in a centralized consolidated report.

```mermaid
stateDiagram-v2
    [*] --> ATSExpert : Entry Point
    ATSExpert --> Recruiter : Edge
    Recruiter --> ResumeReviewer : Edge
    ResumeReviewer --> CareerAdvisor : Edge
    CareerAdvisor --> Consolidator : Edge
    Consolidator --> [*] : END

    state ATSExpert {
        [*] --> EvaluateFormat
        EvaluateFormat --> AssessATSScore
    }
    state Recruiter {
        [*] --> SkillsMatching
        SkillsMatching --> ShortlistDecision
    }
    state ResumeReviewer {
        [*] --> StyleAudit
        StyleAudit --> WritingSuggestions
    }
    state CareerAdvisor {
        [*] --> SuggestRoles
        SuggestRoles --> CertificationsRecommendations
    }
    state Consolidator {
        [*] --> MergeFeedbacks
        MergeFeedbacks --> GenerateFitPercentage
    }
```

---

## Containerized Production Deployment Diagram

```mermaid
graph TB
    subgraph Vercel
        VClient[React Frontend Domain]
    end
    
    subgraph Railway Project Private Network
        Backend[FastAPI Container]
        DB[(PostgreSQL Database)]
        Chroma[(ChromaDB Collection)]
        
        Backend -->|Internal DNS Port 5432| DB
        Backend -->|Internal DNS Port 8000| Chroma
    end
    
    VClient -->|HTTPS Port 443| Backend
    Backend -->|HTTPS Port 443| GeminiAPI[Google Gemini Endpoint]
    Backend -->|TCP Port 5000| MLflow[MLflow Tracker]
```
