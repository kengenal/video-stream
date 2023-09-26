from typing import List

from sqlalchemy.orm import Session

from models.sqlmodels import VideoIndex
from utils.file_loader import VideosFileLoader


def index_videos(db: Session, path: str):
    db.query(VideoIndex).delete()
    file_loader = VideosFileLoader(path=path)

    videos = file_loader.get_videos()
    db.add_all(videos)
    db.commit()


def get_video_index(db: Session, q: str | None) -> List[str]:
    if q is not None:
        return db.query(VideoIndex).filter(VideoIndex.name.like(f"%{q}%")).all()
    return db.query(VideoIndex).all()
