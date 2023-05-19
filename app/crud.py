from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import httpx
from .models import *

async def get_trivia_questions(questions_num: int):
    url = f"https://jservice.io/api/random?count={questions_num}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.json()

async def get_question_ids(session: AsyncSession) -> list[int]:
    result = await session.execute(select(Question.id))
    return result.scalars().all()

async def add_questions(session: AsyncSession, questions: list[Question]) -> list[Question]:
    session.add_all(questions)
    try:
        await session.commit()
        return questions
    except IntegrityError as ex:
        await session.rollback()
        raise IntegrityError("The city is already stored")