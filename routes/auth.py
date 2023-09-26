from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from config.database import get_db
from config.settings import Settings, get_settings
from repositories.user_repository import user_can_be_authentication
from utils.hasher import HasherJwt
from utils.hasher_exceptions import UuidException

router = APIRouter()


class UserModel(BaseModel):
    username: str
    password: str


@router.post("/token/")
async def create_token(
    user: UserModel,
    settings: Annotated[Settings, Depends(get_settings)],
    db: Session = Depends(get_db),
):
    try:
        can_be_auth = user_can_be_authentication(
            db=db, username=user.username, password=user.password
        )
        if can_be_auth is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid credentials",
            )
        token_creator = HasherJwt(
            algorithm=settings.algorytm, secret=settings.token_secret
        )

        return {"token": token_creator.make_secret(public_id=can_be_auth.public_id)}
    except UuidException:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY, detail="Something goes wrong"
        )
