from sqlalchemy.orm import Session

from models.sqlmodels import VideoIndex
from utils.file_loader import VideosFileLoader


def index_videos(db: Session, path: str):
    db.query(VideoIndex).delete()
    file_loader = VideosFileLoader(path=path)

    videos = file_loader.get_videos()
    db.add_all(videos)
    db.commit()
