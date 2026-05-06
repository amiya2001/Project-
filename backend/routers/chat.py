from fastapi import APIRouter
from models.schemas import ChatRequest, ChatResponse
from services.chat_service import chat_service

router = APIRouter(prefix="/api/chat", tags=["Chat"])

@router.post("/", response_model=ChatResponse, summary="Chat with memory")
async def chat(request: ChatRequest):
    result = chat_service.chat(
        session_id=request.session_id,
        message=request.message,
        top_k=request.top_k
    )
    return ChatResponse(**result)

@router.delete("/{session_id}", summary="Clear chat session")
async def clear_session(session_id: str):
    chat_service.clear_session(session_id)
    return {"message": f"Session {session_id} cleared"}