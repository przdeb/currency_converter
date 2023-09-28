import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import declarative_base

load_dotenv()

DATABASE_URL = os.getenv("DB_CONNECTION_STRING", "sqlite:///.sqlite.db")
Base = declarative_base()
engine: Engine = create_engine(DATABASE_URL)
