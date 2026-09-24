from pydantic import BaseModel

class chatResponse(BaseModel):
    message: str