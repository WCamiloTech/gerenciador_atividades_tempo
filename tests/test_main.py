from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_pagina_inicial():
    response = client.get("/")

    assert response.status_code == 200

    dados = response.json()

    assert dados["aplicativo"] == "GAT"
    assert dados["versao"] == "0.1.0"
    assert dados["status"] == "em desenvolvimento"


def test_verificacao_saude():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "servico": "GAT API",
    }


def test_documentacao_openapi():
    response = client.get("/openapi.json")

    assert response.status_code == 200

    dados = response.json()

    assert dados["info"]["title"] == (
        "GAT - Gerenciador de Atividades e Tempo"
    )

    assert "/" in dados["paths"]
    assert "/health" in dados["paths"]