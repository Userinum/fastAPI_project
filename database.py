from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

eng = create_engine("sqlite:///./db.db", connect_args={"check_same_thread": False})
Sess = sessionmaker(bind=eng)
Base = declarative_base()

def get_db():
    db = Sess()
    try:
        yield db
    finally:
        db.close()