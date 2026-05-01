from fastapi import APIRouter


router = APIRouter(prefix="/api/research",tags=["Research"])



@router.get("/topic")
async def topic():
    return ["AI", "Python", "RAG"]