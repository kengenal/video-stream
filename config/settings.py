import os
from enum import StrEnum
from functools import lru_cache

from pydantic_settings import BaseSettings


class StageEnum(StrEnum):
    DEVELOP = "develop"
    PRODUCTION = "production"
    TEST = "test"


class Settings(BaseSettings):
    database_url: str = "sqlite:///./database.db"
    password_secret: str
    token_secret: str
    algorytm: str = "HS256"


class DevSettings(Settings):
    database_url: str = "sqlite:///./database.db"
    password_secret: str = "test"
    token_secret: str = "test"
    algorytm: str = "HS256"


class ProdSettings(Settings):
    pass


class TestSettings(Settings):
    database_url: str = "sqlite:///./test.db"
    password_secret: str
    token_secret: str
    algorytm: str = "HS256"


@lru_cache
def get_settings() -> Settings:
    stage = os.getenv("STAGE", "develop")
    match stage:
        case StageEnum.PRODUCTION:
            return ProdSettings()
        case StageEnum.DEVELOP:
            return DevSettings()
        case StageEnum.TEST:
            return TestSettings()
