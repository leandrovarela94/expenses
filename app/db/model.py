

from db.base import Base
from pydantic import BaseModel
from sqlalchemy import Column, Float, Integer, String


class Entrada(Base):
    __tablename__ = "entradas"

    id = Column(Integer, primary_key=True, index=True)
    descricao = Column(String)
    valor = Column(Float)
    date = Column(String)


class Saida(Base):
    __tablename__ = "saidas"

    id = Column(Integer, primary_key=True, index=True)
    descricao = Column(String)
    valor = Column(Float)
    date = Column(String)
