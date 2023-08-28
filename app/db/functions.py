from datetime import datetime

from db.conections import collection, db
from pydantic import BaseModel


# Modelo Pydantic para as despesas
class DespesaModel(BaseModel):
    nome: str
    valor: float
    data_vencimento: datetime
    prioridade: str

# Função para criar a coleção de despesas (uma vez)


def criar_colecao_despesas():
    if "despesas" not in db.list_collection_names():
        db.create_collection("despesas")
        print("Coleção 'despesas' criada com sucesso.")

# Função para inserir uma despesa


def inserir_despesa(despesa: DespesaModel):
    despesa_dict = despesa.dict()
    result = collection.insert_one(despesa_dict)
    return result.inserted_id

# Função para listar despesas de um mês específico


def listar_despesas_mes(ano: int, mes: int):
    despesas = collection.find({"$expr": {"$eq": [{"$year": "$data_vencimento"}, ano], "$eq": [
                               {"$month": "$data_vencimento"}, mes]}})
    return [DespesaModel(**despesa) for despesa in despesas]

# Função para calcular o total de despesas mensais


def calcular_total_mensal(ano: int, mes: int):
    despesas = collection.find({"$expr": {"$eq": [{"$year": "$data_vencimento"}, ano], "$eq": [
                               {"$month": "$data_vencimento"}, mes]}})
    total = sum(despesa["valor"] for despesa in despesas)
    return total

# Função para calcular o total de despesas por prioridade


def calcular_total_por_prioridade():
    pipeline = [
        {"$group": {"_id": "$prioridade", "total": {"$sum": "$valor"}}}
    ]
    resultado = list(collection.aggregate(pipeline))
    return resultado

# Função para detalhar as despesas do ano todo, mês a mês


def detalhar_despesas_ano(ano: int):
    detalhes_ano = {}
    for mes in range(1, 13):  # Loop pelos meses do ano
        despesas_mes = list(listar_despesas_mes(ano, mes))
        total_mes = calcular_total_mensal(ano, mes)
        detalhes_ano[f"{ano}-{mes:02d}"] = {"despesas": despesas_mes,
                                            "total": total_mes}
    return detalhes_ano
