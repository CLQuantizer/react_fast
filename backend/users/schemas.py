from typing import Union
from pydantic import BaseModel

class JournalBase(BaseModel):
    title: str
    date: Union[str, None] =None
    body: Union[str, None] =None

class JournalCreate(JournalBase):
    pass

class Journal(JournalBase):
    id: int
    author_id: int

    class Config:
       orm_mode = True

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    journals: list[Journal] = []

    class Config:
       orm_mode = True

# class UpdateJournalSchema(BaseModel):
#     title: Optional[str]
#     author: Optional[str]
#     date: Optional[str]
#     body: Optional[str]

#     class Config:
#         orm_mode=True
#         # schema_extra = {
#         #     "example": {
#         #         "title": "ganbarisugita",
#         #         "author": "Ezius",
#         #         "date": "04/07/1967",
#         #         "body": "hello it is me, but updated",
#         #     }
#         # }

# def ResponseModel(data, message):
#     return {
#         "data": [data],
#         "code": 200,
#         "message": message,
#     }


# def ErrorResponseModel(error, code, message):
#     return {"error": error, "code": code, "message": message}

