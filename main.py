from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from database import engine, Base, get_db
from models import User, Task
from auth import hash_password, verify_password, create_token, get_current_user

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.post("/register")
def register(username: str, password: str, db: Session = Depends(get_db)):
    user = User(username=username, password=hash_password(password))
    db.add(user)
    db.commit()
    return {"message": "created"}

@app.post("/login")
def login(username: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()

    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="wrong credentials")

    token = create_token({"user_id": user.id})
    return {"token": token}

@app.post("/tasks")
def create_task(title: str, token: str, db: Session = Depends(get_db)):
    user = get_current_user(token)

    task = Task(
        title=title,
        description="",
        status="todo",
        priority=1,
        user_id=user.id
    )

    db.add(task)
    db.commit()
    return task

@app.get("/tasks")
def get_tasks(token: str, db: Session = Depends(get_db)):
    user = get_current_user(token)
    return db.query(Task).filter(Task.user_id == user.id).all()

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, token: str, db: Session = Depends(get_db)):
    user = get_current_user(token)

    task = db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == user.id
    ).first()
    if task:
        db.delete(task)
        db.commit()
        return {"message": "deleted"}
    return {"error": "not found"}