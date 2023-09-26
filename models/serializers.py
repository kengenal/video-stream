from pydantic.main import BaseModel


class VideoIndexSerializer(BaseModel):
    id: int
    slug: str
    name: str
    full_path: str
    prefix: str

    class Config:
        from_attributes = True
