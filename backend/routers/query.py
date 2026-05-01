from fastapi import APIRouter
from models.schemas import QueryRequest,QueryResponse,QueryResult

router = APIRouter(prefix="/api/query",tags=["Queries"])

@router.post("/search",response_model=QueryResponse,summary="query a doc ")
async def query_document(request: QueryRequest):
    return QueryResponse(query=request.query,
        results=[QueryResult(
                id="chunk_001",
                content="RAG stands for Retrieval Augmented Generation",
                score=0.92,
                metadata={"source": "research.pdf"}
            )
        ])

