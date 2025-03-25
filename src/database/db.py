import os
import threading

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

PG_USER = os.getenv('POSTGRES_USER')
PG_PASS = os.getenv('POSTGRES_PASSWORD')
PG_HOST = os.getenv('POSTGRES_HOST')
PG_PORT = os.getenv('HOST_PORT')
PG_DB = os.getenv('POSTGRES_DB')
DATABASE_URL = f"postgresql+psycopg2://{PG_USER}:{PG_PASS}@{PG_HOST}:{PG_PORT}/{PG_DB}"

Base = declarative_base()

class Database:
    _instance = None
    _lock = threading.Lock()

    def __init__(self):
        if Database._instance is not None:
            raise Exception("This is a singleton class!")
        self.engine = create_engine(DATABASE_URL, echo=True)
        self.SessionLocal = sessionmaker(bind=self.engine)

    @classmethod
    def get_instance(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = cls()
        return cls._instance

    def get_session(self):
        return self.SessionLocal()
