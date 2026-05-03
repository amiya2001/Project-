from pydantic import BaseModel, Field
from typing import Optional

class IngestRequest(BaseModel):
    filename: str
    content: str
    tags: Optional[list[str]]=[]

class IngestResponse (BaseModel):
       
       id: str
       filename: str
       status: str
       chunks_created: int


class QueryRequest(BaseModel):
        
        query: str
        top_k: int = Field(default=5)

class QueryResult(BaseModel):
       
       id : str
       content: str
       score: float
       metadata:dict

class QueryResponse(BaseModel):
        query: str
        answer: str
        sources: list[QueryResult]

class ChatMessage(BaseModel):
        role: str
        content: str

class ChatRequest(BaseModel):
        messages: list [ChatMessage]
        use_knowledge:bool=Field(default=True)


if __name__ == "__main__":
    # Test 1 — without tags (should work now)
    req = IngestRequest(filename="test.pdf", content="hello world")
    print(req)

    # Test 2 — with tags
    req2 = IngestRequest(filename="test.pdf", content="hello world", tags=["AI", "research"])
    print(req2)

    # Test 3 — wrong type should fail (good to see Pydantic catching errors)
    req3 = QueryRequest(query="what is RAG?")
    print(req3)