from sqlmodel import create_engine, SQLModel, Session
from dotenv import load_dotenv
import os

_:bool = load_dotenv()

engine = create_engine(os.getenv("CONNECTION_STRING"), connect_args={"sslmode": "require"}, pool_recycle=300)

def perform_migration():
    SQLModel.metadata.create_all(engine)
    print("Tables created successfully!")

def get_session():
    with Session(engine) as session:
        yield session
