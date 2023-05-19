from pydantic import BaseModel
from datetime import datetime

class QuestionSchema(BaseModel):
    id: int
    question: str
    answer: str
    created_at: datetime

    class Config:
        orm_mode = True