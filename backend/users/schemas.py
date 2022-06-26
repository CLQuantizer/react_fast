from typing import Union
from pydantic import BaseModel

class JournalBase(BaseModel):
    title: str
    date: Union[str, None] =None
    body: Union[str, None] =None

class JournalCreate(JournalBase):
    pass

class JournalDelete(JournalBase):
    title: str

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

class UserInDB(User):
    hashed_password: str

    @classmethod
    def from_dict(cls, d):
        return cls(**d)

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username : Union[str, None ]= None
