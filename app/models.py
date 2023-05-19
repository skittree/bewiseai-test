from sqlalchemy import Column, Integer, String, DateTime
from .db import Base

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True)
    question = Column(String, nullable=False)
    answer = Column(String)
    created_at = Column(DateTime(timezone=True))