from bson import ObjectId
from db.functions import (DespesaModel, calcular_total_mensal,
                          calcular_total_por_prioridade,
                          criar_colecao_despesas, detalhar_despesas_ano,
                          inserir_despesa, listar_despesas_mes)
from fastapi import FastAPI, status
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rota para criar a coleção de despesas (uma vez)


@app.get("/heath")
async def get_health():
    return status.HTTP_200_OK


@app.post("/criar_colecao")
async def criar_colecao():
    criar_colecao_despesas()
    return {"message": "Coleção 'despesas' criada com sucesso."}

# Função personalizada para serializar ObjectId


def custom_json_encoder(obj):
    if isinstance(obj, ObjectId):
        return str(obj)  # Converta ObjectId em uma string
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")


# Substitua o encoder padrão pelo encoder personalizado
app.json_encoder = custom_json_encoder

# Rota para inserir uma despesa


@app.post("/despesas/")
async def criar_despesa(despesa: DespesaModel):
    inserted_id = inserir_despesa(despesa)
    # Converta o ID para uma string
    return {"message": "Despesa inserida com sucesso", "id": str(inserted_id)}

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
