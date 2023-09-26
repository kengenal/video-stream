from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from config.database import get_db
from config.settings import Settings, get_settings
from repositories.user_repository import get_user_by_public_id
from utils.hasher import HasherJwt
from utils.hasher_exceptions import ThisIsNotCorrectTokenException

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/token")


async def get_user(
    settings: Annotated[Settings, Depends(get_settings)],
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Session = Depends(get_db),
):
    hasher = HasherJwt(secret=settings.token_secret, algorithm=settings.algorytm)
    try:
        public_id = hasher.make_unsecret(token=token)
        user = get_user_by_public_id(db=db, public_id=public_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        return user

    except ThisIsNotCorrectTokenException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
