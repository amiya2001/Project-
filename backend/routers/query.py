from fastapi import APIRouter
from models.schemas import QueryRequest,QueryResponse,QueryResult
from services.query_service import query_service

router = APIRouter(prefix="/api/query",tags=["Queries"])

@router.post("/search",response_model=QueryResponse,summary="query a doc ")
async def query_document(request: QueryRequest):
    result=query_service.search(query= request.query,top_k=request.top_k)
    return QueryResponse(**result)

