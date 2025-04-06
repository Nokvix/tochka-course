from pydantic import BaseModel


class Post(BaseModel):
    id: int
    category: int
    title: str
    text: str


class PostUpdate(BaseModel):
    category: int
    text: str
