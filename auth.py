from jose import jwt
from fastapi import HTTPException
import hashlib
import secrets

SECRET = "secret123"
ALG = "HS256"

def h(p):
    s = secrets.token_hex(16)
    return s + ":" + hashlib.sha256((p + s).encode()).hexdigest()

def v(p, hp):
    s, hash_val = hp.split(":")
    return hash_val == hashlib.sha256((p + s).encode()).hexdigest()

def tok(data):
    return jwt.encode(data, SECRET, algorithm=ALG)

def get_u(token, db, User):
    try:
        d = jwt.decode(token, SECRET, algorithms=[ALG])
        return db.query(User).filter(User.id == d["id"]).first()
    except:
        raise HTTPException(status_code=401, detail="bad token")
