from pydantic import BaseModel
from typing import Generic, TypeVar, List

T = TypeVar("T")

class MessageSchema(BaseModel):
    status: str
    message: str

class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    size: int
