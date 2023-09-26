from typing import Optional

from sqlalchemy.orm import Session

from models.sqlmodels import User


def get_user_by_public_id(db: Session, public_id: str) -> Optional[User]:
    potencial_user = db.query(User).filter(User.public_id == public_id).first()
    if not potencial_user:
        return None
    return potencial_user


def user_can_be_authentication(
    db: Session, username: str, password: str
) -> Optional[User]:
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return None
    if user.check_password(password=password) is True:
        return user
    return None
