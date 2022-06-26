from typing import Union
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import APIRouter, Body, Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from pydantic import BaseModel
from datetime import datetime, timedelta
from passlib.context import CryptContext

from . import models, schemas
from .database import(
    create_user,
    create_user_journal,
    delete_journal_by_title,
    delete_user_by_username,
    engine,
    get_journals,
    get_user_journals,
    get_users,
    get_user_by_username,
    SessionLocal,
)

#router config
userRouter = APIRouter()

# db config 
models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Auth config
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# jwt settings
# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception:
        return False

def authenticate_user(username: str, password: str, db: Session=Depends(get_db)):
    user = get_user_by_username(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=25)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session=Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user_by_username(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

# user routes
@userRouter.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session=Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@userRouter.get("/me")
async def read_users_me(current_user: schemas.User = Depends(get_current_user)):
    return current_user

@userRouter.post("/",  response_model=schemas.User)
async def add_new_user(user: schemas.UserCreate, db: Session=Depends(get_db)):
    db_user = get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="username already registered")
    return create_user(db=db, user=user)

@userRouter.get("/", response_model=list[schemas.User], response_description="All users data")
async def read_users_data(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = get_users(db, skip=skip,limit=limit)
    return users

@userRouter.get("/username/{username}", response_model=schemas.User, response_description="One user data retrieved")
async def read_user_data_by_username(username: str, db: Session = Depends(get_db)):
    user = get_user_by_username(db, username=username)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@userRouter.delete("/username/{username}", response_model=schemas.User,response_description="Single user data deleted")
async def delete_user_data_by_username(username: str, db: Session = Depends(get_db)):
    old_user = get_user_by_username(db, username=username)
    if old_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    journals_of_old_user = get_user_journals(db, username=username)
    if len(journals_of_old_user)>0:
        raise HTTPException(status_code=400, detail="User has journals")
    return delete_user_by_username(db=db, username=username)

@userRouter.post("/username/{username}/journals/", response_model=schemas.Journal, response_description="create a journal for a user")
async def add_new_journal_for_user(username: str, journal: schemas.JournalCreate, db: Session = Depends(get_db)):
    return create_user_journal(db=db, journal=journal, username=username)

@userRouter.get("/journals/", response_model=list[schemas.Journal], response_description="get all journals")
async def read_journals_data(db: Session = Depends(get_db)):
    journals = get_journals(db, skip=0, limit=100)
    return journals

@userRouter.get("/username/{username}/journals/", response_model=list[schemas.Journal], response_description="All journals data for a user")
async def read_journals_of_user_by_username(username: str, db: Session = Depends(get_db)):
    return get_user_journals(db=db, username=username)

@userRouter.delete("/username/{username}/journals/", response_model=schemas.Journal, response_description="delete a journal for a user")
async def remove_journal_by_title(journal: schemas.JournalDelete, db: Session = Depends(get_db)):
    return delete_journal_by_title(db=db,title=journal.title)