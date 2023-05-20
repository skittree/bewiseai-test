from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, LargeBinary
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .db import Base
import uuid

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True)
    question = Column(String, nullable=False)
    answer = Column(String)
    created_at = Column(DateTime(timezone=True))

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(UUID(as_uuid=True), default=uuid.uuid4)
    username = Column(String)

class Record(Base):
    __tablename__ = "records"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(Integer, ForeignKey("users.id"))
    audio = Column(LargeBinary)
    
    user = relationship("User", backref="records")