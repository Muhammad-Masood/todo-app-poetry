from sqlmodel import create_engine, SQLModel
from dotenv import load_dotenv
import os

engine = create_engine(os.getenv("CONNECTTION_STRING"), connect_args={"sslmode": "require"}, pool_recycle=300)

def perform_migration():
    SQLModel.metadata.create_all(engine)