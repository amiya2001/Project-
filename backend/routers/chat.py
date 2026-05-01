from fastapi import APIRouter
from models.schemas import ChatRequest

router = APIRouter(prefix="/api/chat",tags=["Chat"])

@router.post("/",response_model=ChatRequest)
async def chat_doc():
    return {"reply": "I am AKS, your knowledge assistant"}