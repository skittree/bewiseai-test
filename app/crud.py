from sqlalchemy.exc import IntegrityError, NoResultFound
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

async def create_questions(session: AsyncSession, questions: list[Question]) -> list[Question]:
    session.add_all(questions)
    try:
        await session.commit()
        return questions
    except IntegrityError as ex:
        await session.rollback()
        raise IntegrityError("Question already in database.", ex.params, ex.orig)

async def create_user(session: AsyncSession, username: str) -> User:
    result = await session.execute(select(User.username).where(User.username == username))
    if result.scalar():
        raise IntegrityError("Username taken.", params=username, orig=result)
    user = User(username=username)
    session.add(user)
    try:
        await session.commit()
        return user
    except IntegrityError as ex:
        await session.rollback()
        raise IntegrityError("User already in database.", ex.params, ex.orig)
    
async def get_user(session: AsyncSession, id: int) -> User:
    result = await session.execute(select(User).where(User.id == id))
    row = result.scalar()
    if row:
        return row
    raise NoResultFound({"statement": "User with specified id was not found.", "params": id})

async def create_record(session: AsyncSession, record: Record) -> Record:
    session.add(record)
    try:
        await session.commit()
        return record
    except IntegrityError as ex:
        await session.rollback()
        raise IntegrityError("Record already in database.", ex.params, ex.orig)
    
async def get_record(session: AsyncSession, uuid: UUID) -> Record:
    result = await session.execute(select(Record).where(Record.id == uuid))
    row = result.scalar()
    if row:
        return row
    raise NoResultFound({"statement": "Record with specified UUID was not found.", "params": uuid})