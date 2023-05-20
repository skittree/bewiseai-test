from starlette.config import Config
from starlette.datastructures import Secret

config = Config(".env")

PROJECT_NAME = "bewiseai-test"
VERSION = "1.0.0"
API_PREFIX = "/api"

QUESTION_LIMIT= config("QUESTION_LIMIT", cast=int)
MAX_FILESIZE_MB = config("MAX_FILESIZE_MB", cast=int)

POSTGRES_USER = config("POSTGRES_USER", cast=str)
POSTGRES_PASSWORD = config("POSTGRES_PASSWORD", cast=Secret)
POSTGRES_SERVER = config("POSTGRES_SERVER", cast=str)
POSTGRES_PORT = config("POSTGRES_PORT", cast=str)
POSTGRES_DB = config("POSTGRES_DB", cast=str)

DATABASE_URL = config(
  "DATABASE_URL",
  cast=str,
  default=f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
)