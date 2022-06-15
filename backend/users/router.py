from fastapi import APIRouter, Body, Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas
from .database import(
    SessionLocal,
    engine,
    get_user,
    get_user_by_username,
    get_users,
    create_user,
    delete_user_by_id,
    delete_user_by_username,
    get_journals,
    create_user_journal,
    delete_journal_by_title,
)


models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

userRouter = APIRouter()

@userRouter.post("/",  response_model=schemas.User)
def add_new_user(user: schemas.UserCreate, db: Session=Depends(get_db)):
    db_user = get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="username already registered")
    return create_user(db=db, user=user)

@userRouter.get("/", response_model=list[schemas.User], response_description="All users data")
def read_users_data(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = get_users(db, skip=skip,limit=limit)
    return users

@userRouter.get("/{user_id}", response_model=schemas.User,response_description="Single user data retrieved")
def read_user_data(user_id: int, db: Session = Depends(get_db)):
    db_user = get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@userRouter.delete("/{user_id}", response_model=schemas.User,response_description="Single user data retrieved")
def delete_user_data_by_id(user_id: int, db: Session = Depends(get_db)):
    old_user = get_user(db, user_id=user_id)
    if old_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return delete_user_by_id(db=db, user_id=user_id)

@userRouter.delete("/", response_model=schemas.User,response_description="Single user data retrieved")
def delete_user_data_by_name(user: schemas.UserBase, db: Session = Depends(get_db)):
    old_user = get_user_by_username(db, username=user.username)
    if old_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return delete_user_by_username(db=db, username=user.username)

@userRouter.post("/{user_id}/journals/", response_model=schemas.Journal, response_description="create a journal for a user")
def add_new_journal_for_user(user_id: int, journal: schemas.JournalCreate, db: Session = Depends(get_db)):
    return create_user_journal(db=db, journal=journal, user_id=user_id)

@userRouter.delete("/{user_id}/journals/", response_model=schemas.Journal, response_description="delete a journal for a user")
def remove_journal_by_title(journal: schemas.JournalBase, db: Session = Depends(get_db)):
    return delete_journal_by_title(db=db,title=journal.title)

@userRouter.get("/journals/", response_model=list[schemas.Journal], response_description="get all journals")
def read_journals_data(db: Session = Depends(get_db)):
    journals = get_journals(db, skip=0, limit=100)
    return journals

