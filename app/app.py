from datetime import date
from typing import List

from db.conections import Session, get_db
from db.model import Entrada, Saida
from fastapi import Depends, FastAPI
from pydantic import BaseModel
from sqlalchemy import func

app = FastAPI()


class Balanco(BaseModel):
    mes: int
    ano: int
    valor_total: float


class EntradaCreate(BaseModel):  # Modelo para criar Entrada
    descricao: str
    valor: float
    date: str  # Data deve ser uma string no formato "YYYY-MM-DD"


class SaidaCreate(BaseModel):  # Modelo para criar Saída
    descricao: str
    valor: float
    date: str  # Data deve ser uma string no formato "YYYY-MM-DD"


class EntradaResponse(BaseModel):  # Modelo de resposta para Entrada
    id: int
    descricao: str
    valor: float
    date: str  # Data deve ser uma string no formato "YYYY-MM-DD"


class SaidaResponse(BaseModel):  # Modelo de resposta para Saída
    id: int
    descricao: str
    valor: float
    date: str  # Data deve ser uma string no formato "YYYY-MM-DD"


@app.post("/entradas/", response_model=EntradaResponse)
def create_entrada(entrada: EntradaCreate, db: Session = Depends(get_db)):

    # Crie uma instância do modelo Entrada
    entrada_db = Entrada(**entrada.dict())
    db.add(entrada_db)
    db.commit()
    db.refresh(entrada_db)
    return entrada_db


@app.post("/saidas/", response_model=SaidaResponse)
def create_saida(saida: SaidaCreate, db: Session = Depends(get_db)):

    saida_db = Saida(**saida.dict())  # Crie uma instância do modelo Saida
    db.add(saida_db)
    db.commit()
    db.refresh(saida_db)
    return saida_db


@app.get("/balanco/{ano}/{mes}")
def get_balanco(ano: int, mes: int, db: Session = Depends(get_db)):
    first_day = f"{ano}-{mes:02d}-01"  # Formato YYYY-MM-DD
    next_month = mes + 1 if mes < 12 else 1
    next_year = ano + 1 if mes == 12 else ano
    last_day = f"{next_year}-{next_month:02d}-01"  # Formato YYYY-MM-DD

    entradas = db.query(Entrada).filter(
        Entrada.date >= first_day, Entrada.date < last_day).all()
    saidas = db.query(Saida).filter(
        Saida.date >= first_day, Saida.date < last_day).all()

    total_entradas = sum(entrada.valor for entrada in entradas)
    total_saidas = sum(saida.valor for saida in saidas)

    balanco = Balanco(mes=mes, ano=ano,
                      valor_total=total_entradas - total_saidas)

    return balanco
