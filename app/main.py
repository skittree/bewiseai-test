from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import FastAPI, APIRouter, status, Depends, HTTPException
from datetime import datetime
from . import crud
from .config import QUESTION_LIMIT
from .models import Question
from .schemas import QuestionSchema
from .db import get_session, init_models

app = FastAPI()
trivia_router = APIRouter()

@app.on_event("startup")
async def startup():
    await init_models()

@trivia_router.post('/', status_code=status.HTTP_201_CREATED)
async def save_trivia(questions_num: int, session: AsyncSession = Depends(get_session)):
    if questions_num > QUESTION_LIMIT:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Question limit exceeded. Maximum allowed: {QUESTION_LIMIT}",
        )
    
    existing_question_ids = set(await crud.get_question_ids(session))
    questions = []
    # can potentially run into an endless loop if our database has ALL questions from the API
    while len(questions) < questions_num:
        data = await crud.get_trivia_questions(questions_num - len(questions))
        for question_data in data:
            if question_data['id'] not in existing_question_ids:
                existing_question_ids.add(question_data['id'])
                created_at = datetime.strptime(question_data['created_at'], "%Y-%m-%dT%H:%M:%S.%fZ")
                question_data['created_at'] = created_at
                question = Question(**question_data)
                questions.append(question)

    if questions:
        await crud.add_questions(session, questions)

    return [QuestionSchema.from_orm(q) for q in questions]

app.include_router(trivia_router, tags=['Trivia'], prefix='/api/trivia')