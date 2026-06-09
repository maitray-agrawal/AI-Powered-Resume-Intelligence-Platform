from fastapi import APIRouter, status, HTTPException
from app.schemas.rag import RAGIngestRequest, RAGIngestResponse, RAGChatRequest, RAGChatResponse
from app.services.rag_service import ResumeRAGService

router = APIRouter()


@router.post(
    "/ingest",
    response_model=RAGIngestResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Ingest resume text into RAG vector store",
    description="Accepts resume raw text and splits it into semantic chunks, indexing them in ChromaDB."
)
def ingest_resume(request: RAGIngestRequest):
    chunks = ResumeRAGService.ingest_resume(
        resume_id=request.resume_id,
        resume_text=request.resume_text
    )
    if chunks == 0:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to ingest resume chunks into vector store."
        )
    return {"success": True, "num_chunks": chunks}


@router.post(
    "/chat",
    response_model=RAGChatResponse,
    status_code=status.HTTP_200_OK,
    summary="Chat with an ingested resume contextually",
    description="Queries Chroma DB for the specific resume's chunks, retrieves context, and queries Gemini for answers."
)
def chat_with_resume(request: RAGChatRequest):
    answer, sources = ResumeRAGService.chat_with_resume(
        resume_id=request.resume_id,
        query=request.query
    )
    return {"answer": answer, "sources": sources}
