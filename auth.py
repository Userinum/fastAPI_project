from jose import jwt
from passlib.context import CryptContext
from fastapi import HTTPException
import hashlib

SECRET = "secret123"
ALG = "HS256"

pwd = CryptContext(schemes=["bcrypt"])

def h(p):
    p = hashlib.sha256(p.encode()).hexdigest()
    return pwd.hash(p)

def v(p, hp):
    p = hashlib.sha256(p.encode()).hexdigest()
    try:
        return pwd.verify(p, hp)
    except:
        pwd.verify(p[:72], hp)

def tok(data):
    return jwt.encode(data, SECRET, algorithm=ALG)

def get_u(token, db, User):
    try:
        d = jwt.decode(token, SECRET, algorithms=[ALG])
        return db.query(User).filter(User.id == d["id"]).first()
    except:
        raise HTTPException(status_code=401, detail="bad token")
