from fastapi import APIRouter
from app.services.chatService import chat
from app.model.chatRequest import chatRequest
from fastapi.responses import StreamingResponse

router = APIRouter()

@router.post('/chat')
def stream_chat(request:chatRequest):
    return StreamingResponse(
        chat(
            session_id= request.session_id,
            user_message= request.message 
        ),
        media_type="text/plain"
    )