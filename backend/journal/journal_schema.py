from typing import Optional
from pydantic import BaseModel, EmailStr, Field

class JournalSchema(BaseModel):
    title: str = Field(...)
    author: str= Field(...)
    date: str = Field(...)
    body: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "title": "ganbaru",
                "author": "Ezio",
                "date": "02/05/1987",
                "body": "hello it is me",
            }
        }

class UpdateJournalSchema(BaseModel):
    title: Optional[str]
    author: Optional[str]
    date: Optional[str]
    body: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "title": "ganbarisugita",
                "author": "Ezius",
                "date": "04/07/1967",
                "body": "hello it is me, but updated",
            }
        }

def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}

