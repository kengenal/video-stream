import os
from typing import Annotated

from fastapi import (APIRouter, BackgroundTasks, Depends, Header,
                     HTTPException, status)
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from config.database import get_db
from config.settings import Settings, get_settings
from dependencies.auth_dependencies import get_user
from models.serializers import VideoIndexSerializer
from models.sqlmodels import User
from repositories.video_repository import (get_video_by_slug, get_video_index,
                                           index_videos)
from utils.streaming import send_bytes_file, send_bytes_range

router = APIRouter()


@router.get("/videos/")
async def get_videos(
    _: Annotated[User, Depends(get_user)],
    db: Session = Depends(get_db),
    q: str | None = None,
):
    items = get_video_index(db=db, q=q)
    return {"results": [VideoIndexSerializer.model_validate(x) for x in items]}


@router.get("/videos/index/")
async def index(
    background_task: BackgroundTasks,
    settings: Annotated[Settings, Depends(get_settings)],
    _: Annotated[User, Depends(get_user)],
    db: Session = Depends(get_db),
):
    background_task.add_task(index_videos, db=db, path=settings.video_path)
    return {"OK": "idenxing adding to queue"}


@router.get("/videos/{slug}/")
async def stream(
    slug: str,
    _: Annotated[User, Depends(get_user)],
    db: Session = Depends(get_db),
    range: Annotated[str | None, Header()] = None,
):
    video = get_video_by_slug(db=db, slug=slug)
    if not video:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Video not Found"
        )
    size = os.stat(video.full_path).st_size

    if range:
        parts = range.replace("bytes=", "").split("-")
        start = int(parts[0]) if parts[0].isdigit() else 0
        end = int(parts[1]) if parts[1].isdigit() else size - 1

        chunk_size = end - start + 1
        headers = {
            "Accept-Ranges": "bytes",
            "Content-Range": f"bytes {str(start)}-{str(end)}/{str(size)}",
            "Content-Length": str(chunk_size),
            "access-control-expose-headers": (
                "content-type, accept-ranges, content-length, "
                "content-range, content-encoding"
            ),
        }

        return StreamingResponse(
            send_bytes_range(video.full_path, start, end),
            media_type="video/mp4",
            headers=headers,
            status_code=status.HTTP_206_PARTIAL_CONTENT,
        )
    return StreamingResponse(
        send_bytes_file(video.full_path),
        media_type="video/mp4",
        headers={"Content-Length": str(size)},
        status_code=status.HTTP_206_PARTIAL_CONTENT,
    )
