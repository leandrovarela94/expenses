
import logging

import datadog
import ddtrace
from db.functions import (calcular_total_mensal, calcular_total_por_prioridade,
                          criar_colecao_despesas, detalhar_despesas_ano,
                          inserir_despesa, listar_despesas_mes)
from dto.DespesasDTO import Despesas
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

datadog.initialize(
    api_key='b3cc1d2b39bebd20716385298d626487', hostname='agent-hostname', port=8126)

# Configuração do logger para enviar logs para o Datadog
ddtrace.config.logs_injection = True
ddtrace.config.logs_enabled = True


logging.getLogger(__name__)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rota para criar a coleção de despesas (uma vez)
logger = logging.getLogger(__name__)


@app.get("/")
async def read_root():
    # Crie um span para esta requisição
    # Execute o código da requisição aqui
    return {"message": "Hello, World"}


@app.get("/heath")
async def get_health():
    return status.HTTP_200_OK


@app.post("/criar_colecao")
async def criar_colecao():
    criar_colecao_despesas()
    return {"message": "Coleção 'despesas' criada com sucesso."}

# Inicialize o tracer do Datadog


@app.post("/despesas")
async def criar_despesa(despesa: Despesas, request: Request):

    inserted_id = inserir_despesa(despesa)
    status_code = request.scope.get("status_code", None)

    if status_code == 200:
        # Lógica para quando o código de status for 200 OK
        logger.info(
            f" message: Despesa inserida com sucesso, id: {str(inserted_id)} ")

    elif status_code == 400:
        # Lógica para quando o código de status for 400 Bad Request
        logger.error(
            f"message: Um dos campos foi passado incorretamente, body: {request.scope.items()} ")

    else:
        logger.error(
            f"message: Um dos campos foi passado incorretamente, body: {request.scope.items()} ")

    return status.HTTP_200_OK

# Rota para listar despesas de um mês específico


@app.get("/despesas/{ano}/{mes}")
async def listar_despesas(ano: int, mes: int):
    despesas = listar_despesas_mes(ano, mes)
    return despesas

# Rota para calcular o total de despesas mensais


@app.get("/total/{ano}/{mes}")
async def calcular_total(ano: int, mes: int):
    total = calcular_total_mensal(ano, mes)
    return {"total": total}

# Rota para calcular o total de despesas por prioridade


@app.get("/total/prioridade")
async def calcular_total_prioridade():
    total_por_prioridade = calcular_total_por_prioridade()
    return total_por_prioridade

# Rota para detalhar as despesas do ano todo, mês a mês


@app.get("/detalhes/{ano}")
async def detalhar_despesas(ano: int):
    detalhes = detalhar_despesas_ano(ano)
    return detalhes
