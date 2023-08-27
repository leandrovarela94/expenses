import pytest
from db.functions import DespesaModel, collection, criar_colecao_despesas
from fastapi.testclient import TestClient
from pymongo import MongoClient

from app.app import app

# Configuração do MongoDB para testes
test_client = TestClient(app)
test_db_name = "test_despesas"
test_client = MongoClient(f"mongodb://localhost:27017/{test_db_name}")

# Modelo Pydantic para testes


class TestDespesaModel(DespesaModel):
    id: str

# Fixture para criar a coleção de despesas para testes


@pytest.fixture(scope="module", autouse=True)
def setup_teardown_test_db():
    # Configura a coleção de despesas para testes
    test_db = test_client[test_db_name]
    test_collection = test_db["despesas"]
    criar_colecao_despesas(test_db, test_collection)

    yield

    # Remove a coleção após os testes
    test_db.drop_collection("despesas")

# Casos de teste


def test_inserir_despesa():
    despesa = {
        "nome": "Aluguel",
        "valor": 1000.0,
        "data_vencimento": "2023-08-01",
        "prioridade": "Alta"
    }
    response = test_client.post("/despesas/", json=despesa)
    assert response.status_code == 200


def test_listar_despesas_mes():
    # Inserir uma despesa de teste para o mês de agosto de 2023
    test_client.post("/despesas/", json={
        "nome": "Aluguel",
        "valor": 1000.0,
        "data_vencimento": "2023-08-01",
        "prioridade": "Alta"
    })

    response = test_client.get("/despesas/2023/8")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1


def test_calcular_total_mensal():
    # Inserir despesas de teste para o mês de agosto de 2023
    test_client.post("/despesas/", json={
        "nome": "Aluguel",
        "valor": 1000.0,
        "data_vencimento": "2023-08-01",
        "prioridade": "Alta"
    })
    test_client.post("/despesas/", json={
        "nome": "Comida",
        "valor": 500.0,
        "data_vencimento": "2023-08-10",
        "prioridade": "Média"
    })

    response = test_client.get("/total/2023/8")
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert data["total"] == 1500.0


def test_calcular_total_por_prioridade():
    # Inserir despesas de teste com diferentes prioridades
    test_client.post("/despesas/", json={
        "nome": "Aluguel",
        "valor": 1000.0,
        "data_vencimento": "2023-08-01",
        "prioridade": "Alta"
    })
    test_client.post("/despesas/", json={
        "nome": "Comida",
        "valor": 500.0,
        "data_vencimento": "2023-08-10",
        "prioridade": "Média"
    })

    response = test_client.get("/total/prioridade")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2


def test_detalhar_despesas_ano():
    # Inserir despesas de teste para diferentes meses de 2023
    test_client.post("/despesas/", json={
        "nome": "Aluguel",
        "valor": 1000.0,
        "data_vencimento": "2023-08-01",
        "prioridade": "Alta"
    })
    test_client.post("/despesas/", json={
        "nome": "Comida",
        "valor": 500.0,
        "data_vencimento": "2023-09-10",
        "prioridade": "Média"
    })

    response = test_client.get("/detalhes/2023")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 12
