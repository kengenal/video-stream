from uuid import uuid4

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from config.database import Base
from config.settings import get_settings
from utils.hasher import HasherPassword


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    public_id: Mapped[str] = mapped_column(String(255), default=str(uuid4()))
    username: Mapped[str] = mapped_column(String(100))
    password: Mapped[str] = mapped_column(String(100))

    def __repl__(self):
        return self.username

    def make_password(self, password: str):
        salt = get_settings().password_secret
        hasher = HasherPassword(salt=salt)
        self.password = hasher.make_secret(password=password)

    def check_password(self, password: str) -> bool:
        salt = get_settings().password_secret
        hasher = HasherPassword(salt=salt)
        return hasher.check(password=password, hash=self.password)


class VideoIndex(Base):
    __tablename__ = "video_index"
