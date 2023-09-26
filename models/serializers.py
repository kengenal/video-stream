from pydantic.main import BaseModel, ConfigDict


class VideoIndexSerializer(BaseModel):
    id: int
    slug: str
    name: str
    full_path: str
    prefix: str

    model_config = ConfigDict(from_attributes=True)
