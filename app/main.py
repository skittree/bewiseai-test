from io import BytesIO
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, NoResultFound
from fastapi import FastAPI, APIRouter, Request, status, Depends, HTTPException, Form, File, UploadFile
from fastapi.responses import Response, RedirectResponse
from datetime import datetime
from . import crud
from .config import QUESTION_LIMIT
from .models import *
from .schemas import *
from .db import get_session, init_models
from pydub import AudioSegment

app = FastAPI()
trivia_router = APIRouter()
user_router = APIRouter()
record_router = APIRouter()

@app.on_event("startup")
async def startup():
    await init_models()

@trivia_router.post('/', response_model=list[QuestionSchema], status_code=status.HTTP_201_CREATED)
async def create_questions(questions_num: int, session: AsyncSession = Depends(get_session)):
    """
    Gets `questions_num` questions from the [jService API](https://jservice.io) and saves them to the database. Returns saved questions.
    """
    # add exception for 0 questions?
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
        try:
            await crud.create_questions(session, questions)
        except IntegrityError as ex:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"statement": ex.statement, "params": ex.params},
            )

    return [QuestionSchema.from_orm(q) for q in questions]

@user_router.post('/', response_model=UserSchema, status_code=status.HTTP_201_CREATED)
async def create_user(username: str = Form(...), session: AsyncSession = Depends(get_session)):
    """
    Creates a user via `username` if it does not exist in the database. Returns the `id` and UUID `token` for the created user.
    """
    try:
        user = await crud.create_user(session, username)
    except IntegrityError as ex:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"statement": ex.statement, "params": ex.params},
        )
    return UserSchema.from_orm(user)

@record_router.get('/', status_code=status.HTTP_200_OK)
async def get_record(id: UUID, user_id: int, session: AsyncSession = Depends(get_session)):
    """
    Downloads an .mp3 file stored in the database via provided UUID `id` and user id `user_id`.
    """
    try:
        user = await crud.get_user(session, user_id)
        record = await crud.get_record(session, id)
    except NoResultFound as ex:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ex.args,
        )
    if user.id != record.user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"statement": "The audiofile does not belong to the specified user", "params": [str(id), user_id]},
        )
    headers = {'Content-Disposition': f'inline; filename="{id}.mp3"'}
    return Response(record.audio, headers=headers, media_type='audio/mpeg')

@record_router.post('/', status_code=status.HTTP_201_CREATED)
async def create_record(request: Request, user_id: int = Form(...), user_token: UUID = Form(...), audio: UploadFile = File(...), session: AsyncSession = Depends(get_session)):
    """
    Saves .wav `audio` in the database as .mp3 for the specified `user_id` with `user_token` UUID validation. Returns download link.
    """
    try:
        user = await crud.get_user(session, user_id)
    except NoResultFound as ex:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ex.args,
        )
    
    if user_token != user.token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid UUID token provided.",
        )

    type, ext = audio.content_type.split("/")

    if type != "audio":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"statement": "Please upload a valid .wav audio file.", "params": type},
        )
    if ext != "wav":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"statement": "This audio file is incompatible, please upload .wav audio.", "params": ext},
        )
    
    sound = AudioSegment.from_wav(BytesIO(await audio.read())).export(format="mp3").read()
    record = await crud.create_record(session, Record(user_id=user_id, audio=sound))
    return request.url_for("get_record").include_query_params(id=record.id, user_id=user_id)

app.include_router(trivia_router, tags=['Trivia'], prefix='/api/trivia')
app.include_router(user_router, tags=['Users'], prefix='/api/user')
app.include_router(record_router, tags=['Records'], prefix='/api/record')