# tests/test_main.py
from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


def test_create_entrada():
    response = client.post(
        "/entradas/", json={"descricao": "Salário", "valor": 3000.0, "data": "2023-08-01"})
    assert response.status_code == 200
    assert response.json()["descricao"] == "Salário"


def test_create_saida():
    response = client.post(
        "/saidas/", json={"descricao": "Aluguel", "valor": 1000.0, "data": "2023-08-05"})
    assert response.status_code == 200
    assert response.json()["descricao"] == "Aluguel"


def test_get_balanco():
    response = client.get("/balanco/2023/8")
    assert response.status_code == 200
    assert response.json()["mes"] == 8
    assert response.json()["ano"] == 2023
