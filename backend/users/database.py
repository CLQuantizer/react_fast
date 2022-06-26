from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from jose import JWTError, jwt
from passlib.context import CryptContext
from . import models, schemas

SQLALCHEMY_DATABASE_URL = "postgresql://ezio:password@localhost:5432/ezio"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# hash operation
def get_password_hash(password):
    return pwd_context.hash(password)

# the CRUD operations
def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    new_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def delete_user_by_username(db: Session, username:str):
    old_user = get_user_by_username(db=db,username=username)
    db.delete(old_user)
    db.commit()
    return old_user

def create_user_journal(db: Session, journal: schemas.JournalCreate, username: str):
    user = get_user_by_username(db=db, username=username)
    new_journal = models.Journal(**journal.dict(), author_id=user.id)
    db.add(new_journal)
    db.commit()
    db.refresh(new_journal)
    return new_journal

def get_user_journals(db: Session, username: str):
    user = get_user_by_username(db=db, username=username)
    return db.query(models.Journal).filter(models.Journal.author_id == user.id).all()

def get_journals(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Journal).offset(skip).limit(limit).all()

def get_journal_by_title(db: Session, title: str):
    return db.query(models.Journal).filter(models.Journal.title == title).first()

def delete_journal_by_title(db: Session, title: str):
    journal = get_journal_by_title(db=db, title=title)
    db.delete(journal)
    db.commit()
    return journal