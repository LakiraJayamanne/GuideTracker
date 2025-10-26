from sqlmodel import SQLModel, create_engine, Session
from models import Position  # ✅ This line makes the model visible

DATABASE_URL = "sqlite:///positions.db"
engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
