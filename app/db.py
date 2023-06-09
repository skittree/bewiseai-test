from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from .config import DATABASE_URL
from sqlalchemy.ext.declarative import declarative_base

def _declarative_constructor(self, **kwargs):
    """Don't raise a TypeError for unknown attribute names."""
    cls_ = type(self)
    for k in kwargs:
        if not hasattr(cls_, k):
            continue
        setattr(self, k, kwargs[k])

engine = create_async_engine(DATABASE_URL, echo=True)
Base = declarative_base(constructor=_declarative_constructor)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session

async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)