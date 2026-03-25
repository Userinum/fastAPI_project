from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from db import eng, Base, get_db
from models import User, Task
from auth import hash_password, verify_password, create_token, get_current_user

app = FastAPI()
Base.metadata.create_all(bind=eng)

@app.post("/register")
def register(name: str, password: str, db: Session = Depends(get_db)):
    user = User(name=name, password=hash_password(password))
    db.add(user)
    db.commit()
    return {"Все прошло четко!": 1}

@app.post("/login")
def login(name: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.name == name).first()
    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=401)
    return {"token": create_token({"id": user.id})}

@app.post("/add_tasks")
def create_task(title: str, token: str, db: Session = Depends(get_db)):
    user = get_current_user(token, db, User)
    task = Task(title=title, description="", status ="todo", priority=1, user_id=user.id)
    db.add(task)
    db.commit()
    return task

@app.get("/get_tasks")
def get_tasks(token: str, db: Session = Depends(get_db)):
    user = get_current_user(token, db, User)
    return db.query(Task).filter(Task.user_id == user.id).all()

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, token: str, db: Session = Depends(get_db)):
    user = get_current_user(token, db, User)
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == user.id).first()
    if task:
        db.delete(task)
        db.commit()
        return {"Все прошло четко!": 1}
    return {"Не все ок!": 1}

@app.get("/search")
def search_tasks(query: str, token: str, db: Session = Depends(get_db)):
    user = get_current_user(token, db, User)
    return db.query(Task).filter(Task.user_id == user.id, (Task.title.contains(query) | Task.description.contains(query))).all()

@app.get("/top")
def get_top_tasks(limit: int, token: str, db: Session = Depends(get_db)):
    user = get_current_user(token, db, User)
    return db.query(Task).filter(Task.user_id == user.id).order_by(Task.priority.desc()).limit(limit).all()

@app.get("/")
def root():
    return {"ok": "yes"}
