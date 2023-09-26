from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Depends
from sqlalchemy.orm import Session

from config.database import get_db
from config.settings import Settings, get_settings
from dependencies.auth_dependencies import get_user
from models.sqlmodels import User
from repositories.video_repository import index_videos

router = APIRouter()


@router.get("/videos/")
async def get_videos(
    user: Annotated[User, Depends(get_user)],
    db: Session = Depends(get_db),
):
    return {"test": user.username}


@router.get("/videos/index/")
async def index(
    background_task: BackgroundTasks,
    settings: Annotated[Settings, Depends(get_settings)],
    user: Annotated[User, Depends(get_user)],
    db: Session = Depends(get_db),
):
    background_task.add_task(index_videos, db=db, path=settings.video_path)
    return {"OK": "idenxing adding to queue"}
