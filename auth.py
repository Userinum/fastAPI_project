from jose import jwt
from fastapi import HTTPException
import hashlib
import secrets

SECRET_KEY = "secret123"
ALGORITHM = "HS256"

def hash_password(password):
    s = secrets.token_hex(16)
    return s + ":" + hashlib.sha256((password + s).encode()).hexdigest()

def verify_password(password, hashed_password):
    s, hash_value = hashed_password.split(":")
    return hash_value == hashlib.sha256((password + s).encode()).hexdigest()

def create_token(data):
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token, db, User):
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return db.query(User).filter(User.id == decoded["id"]).first()
    except:
        raise HTTPException(status_code=401, detail="Invalid token")
