from jose import jwt
from passlib.context import CryptContext
from fastapi import HTTPException
from sqlalchemy.orm import Session
from models import User
import os

SECRET = os.getenv("SECRET_KEY", "secret123")
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_pwd(password: str) -> str:
    return pwd_context.hash(password)

def check_pwd(password: str, hashed: str) -> bool:
    return pwd_context.verify(password, hashed)

def create_token(data: dict) -> str:
    return jwt.encode(data, SECRET, algorithm=ALGORITHM)

def get_current_user(token: str, db: Session):
    try:
        data = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        user = db.query(User).filter(User.id == data["user_id"]).first()
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")