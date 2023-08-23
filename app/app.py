from datetime import date
from typing import List

from db.conections import Session, get_db
from db.model import Balanco, Entrada, EntradaModel, Saida, SaidaModel
from fastapi import Depends, FastAPI
from sqlalchemy import func

app = FastAPI()


@app.post("/entradas/")
def create_entrada(entrada: EntradaModel, db: Session = Depends(get_db)):
    db_entrada = Entrada(**entrada.dict())
    db.add(db_entrada)
    db.commit()
    db.refresh(entrada)
    return entrada


@app.post("/saidas/", response_model=SaidaModel)
def create_saida(saida: SaidaModel, db: Session = Depends(get_db)):
    db_saida = Saida(**saida.dict())
    db.add(db_saida)
    db.commit()
    db.refresh(saida)
    return saida


@app.get("/balanco/{ano}/{mes}")
def get_balanco(ano: int, mes: int, db: Session = Depends(get_db)):
    first_day = date(ano, mes, 1)
    last_day = date(ano, mes + 1, 1) if mes < 12 else date(ano + 1, 1, 1)

    entradas = db.query(Entrada).filter(
        Entrada.data >= first_day, Entrada.data < last_day).all()
    saidas = db.query(Saida).filter(
        Saida.data >= first_day, Saida.data < last_day).all()

    total_entradas = sum(entrada.valor for entrada in entradas)
    total_saidas = sum(saida.valor for saida in saidas)

    balanco = Balanco(mes=mes, ano=ano,
                      valor_total=total_entradas - total_saidas)

    return balanco
