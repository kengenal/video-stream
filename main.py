
from fastapi import FastAPI

from routes import auth, video

app = FastAPI()

app.include_router(auth.router, prefix="/api/v1")
app.include_router(video.router, prefix="/api/v1")
