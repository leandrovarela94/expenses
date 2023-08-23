# conections.py
import os

from db.base import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

database_url = 'postgresql://postgres:Qh8h9Sz1iWKKSlL4lDvR@containers-us-west-81.railway.app:5531/railway'
engine = create_engine(database_url)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()


Session()
