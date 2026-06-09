import chromadb
from chromadb.config import Settings as ChromaSettings
from typing import List, Dict, Any, Optional

from app.core.config import settings


class ChromaDBService:
    def __init__(self):
        self._client = None

    @property
    def client(self):
        if self._client is None:
            self._client = chromadb.HttpClient(
                host=settings.CHROMA_HOST,
                port=str(settings.CHROMA_PORT),
                settings=ChromaSettings(allow_reset=True)
            )
        return self._client

    def get_or_create_collection(self, name: str):
        """
        Retrieves or creates a specific collection in ChromaDB.
        """
        return self.client.get_or_create_collection(name=name)

    def add_vectors(
        self,
        collection_name: str,
        ids: List[str],
        embeddings: List[List[float]],
        metadatas: Optional[List[Dict[str, Any]]] = None,
        documents: Optional[List[str]] = None
    ) -> None:
        """
        Adds vector representations and corresponding metadata documents to a collection.
        """
        collection = self.get_or_create_collection(collection_name)
        collection.add(
            ids=ids,
            embeddings=embeddings,
            metadatas=metadatas,
            documents=documents
        )

    def query_similarity(
        self,
        collection_name: str,
        query_embeddings: List[List[float]],
        n_results: int = 5,
        where: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Executes a similarity search against the vectors stored in the collection.
        """
        collection = self.get_or_create_collection(collection_name)
        return collection.query(
            query_embeddings=query_embeddings,
            n_results=n_results,
            where=where
        )


# Global service instance
vector_db_service = ChromaDBService()
