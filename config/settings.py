import os
from enum import StrEnum
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class StageEnum(StrEnum):
    DEVELOP = "develop"
    PRODUCTION = "production"
    TEST = "test"


class Settings(BaseSettings):
    database_url: str = "sqlite:///./database.db"
    algorytm: str = "HS256"
    password_secret: str
    token_secret: str
    video_path: str

    model_config = SettingsConfigDict(env_file=".env")


class DevSettings(Settings):
    database_url: str = "sqlite:///./database.db"
    algorytm: str = "HS256"
    password_secret: str
    token_secret: str
    video_path: str


class ProdSettings(Settings):
    pass


class TestSettings(Settings):
    database_url: str = "sqlite:///./test.db"
    algorytm: str = "HS256"
    password_secret: str
    token_secret: str
    video_path: str


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
