from pydantic import BaseModel
from typing import List


class TextPostSchema(BaseModel):
    id: int
    content: str
    parent_id: int | type(None)

    class Config:
        orm_mode = True


class SubmitPostSchema(BaseModel):
    content: str

    class Config:
        orm_mode = True


class ListPostsSchema(BaseModel):
    id: int
    content: str
    replies: List["TextPostSchema"]

    class Config:
        orm_mode = True
