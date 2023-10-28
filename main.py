from getpass import getpass

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typer import Typer

from routes import auth, video

app = FastAPI()
command = Typer()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth.router, prefix="/api/v1")
app.include_router(video.router, prefix="/api/v1")


@command.command()
def createuser():
    from config.database import SessionLocal
    from repositories.user_repository import create_user

    session = SessionLocal()
    username = input("username: ")
    password = getpass("password: ")
    create_user(db=session, username=username, password=password)
    session.close()
    print("User has been create")


@command.command()
def serve():
    print(
        """
    Use this only for dev
        """
    )
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


def main():
    command()


if __name__ == "__main__":
    main()
