from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

class QuestionSchema(BaseModel):
    id: int
    question: str
    answer: str
    created_at: datetime

    class Config:
        orm_mode = True

class UserSchema(BaseModel):
    id: int
    token: UUID

    class Config:
        orm_mode = True