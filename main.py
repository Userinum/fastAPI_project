from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from db import eng, Base, get_db
from models import User, Task
from auth import h, v, tok, get_u

app = FastAPI()
Base.metadata.create_all(bind=eng)

@app.post("/reg")
def reg(name: str, pwd: str, db: Session = Depends(get_db)):
    u = User(name=name, pwd=h(pwd))
    db.add(u)
    db.commit()
    return {"ok": 1}

@app.post("/login")
def login(name: str, pwd: str, db: Session = Depends(get_db)):
    u = db.query(User).filter(User.name == name).first()
    if not u or not v(pwd, u.pwd):
        raise HTTPException(status_code=401)
    return {"t": tok({"id": u.id})}

@app.post("/add")
def add(title: str, t: str, db: Session = Depends(get_db)):
    u = get_u(t, db, User)
    task = Task(title=title, text="", st="todo", pr=1, uid=u.id)
    db.add(task)
    db.commit()
    return task

@app.get("/all")
def all(t: str, db: Session = Depends(get_db)):
    u = get_u(t, db, User)
    return db.query(Task).filter(Task.uid == u.id).all()

@app.delete("/del/{id}")
def delete(id: int, t: str, db: Session = Depends(get_db)):
    u = get_u(t, db, User)
    task = db.query(Task).filter(Task.id == id, Task.uid == u.id).first()
    if task:
        db.delete(task)
        db.commit()
        return {"ok": 1}
    return {"err": 1}

@app.get("/find")
def find(q: str, t: str, db: Session = Depends(get_db)):
    u = get_u(t, db, User)
    return db.query(Task).filter(
        Task.uid == u.id,
        (Task.title.contains(q) | Task.text.contains(q))
    ).all()

@app.get("/top")
def top(n: int, t: str, db: Session = Depends(get_db)):
    u = get_u(t, db, User)
    return db.query(Task)\
        .filter(Task.uid == u.id)\
        .order_by(Task.pr.desc())\
        .limit(n)\
        .all()

@app.get("/")
def root():
    return {"ok": "yes"}