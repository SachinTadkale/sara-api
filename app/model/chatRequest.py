from pydantic import BaseModel

class chatRequest(BaseModel):
    session_id: str
    message: str