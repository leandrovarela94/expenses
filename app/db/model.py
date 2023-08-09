
from datetime import datetime

from db.base import Base
from sqlalchemy import Column, DateTime, Float, Integer, String


class Expenses(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    expense_name = Column(String, index=True)
    month = Column(Integer, index=True)
    year = Column(Integer, index=True)
    description = Column(String, nullable=True)
    date = Column(DateTime, default=datetime.now, index=True)
    value = Column(Float)
