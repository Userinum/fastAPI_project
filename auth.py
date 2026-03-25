from jose import jwt
from passlib.context import CryptContext
from fastapi import HTTPException
from models import User
from database import SessionLocal

SECRET_KEY = "secret123"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"])

def hash_password(password):
    return pwd_context.hash(password)

def verify_password(password, hashed):
    return pwd_context.verify(password, hashed)

def create_token(data: dict):
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str):
    db = SessionLocal()
    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user = db.query(User).filter(User.id == data["user_id"]).first()
        return user
    except:
        raise HTTPException(status_code=401, detail="Invalid token")