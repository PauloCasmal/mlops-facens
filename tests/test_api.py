"""Testes da API. Usam um modelo falso: não dependem do MLflow nem da rede."""
import json

import numpy as np
import pytest
from fastapi.testclient import TestClient

import api.main as main
from bike import FEATURES

EXEMPLO = json.load(open("api/exemplo.json"))


class ModeloFalso:
    """Responde sempre o mesmo valor: o que testamos aqui é a API, não o modelo."""

    def predict(self, X):
        return np.full(len(X), 123.4)


@pytest.fixture
def client(monkeypatch):
    monkeypatch.setattr(main, "carregar_modelo", lambda: (ModeloFalso(), "teste"))
    with TestClient(main.app) as c:
        yield c


def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["model_version"] == "teste"


def test_predict(client):
    r = client.post("/predict", json=EXEMPLO)
    assert r.status_code == 200
    assert r.json() == {"cnt": 123, "model_version": "teste"}


def test_hora_invalida(client):
    hora_errada = {**EXEMPLO, "hr": 25}
    # TODO: mande a hora_errada (como o test_predict manda o EXEMPLO) e confira o código de erro
    r = client.post("/predict", json=hora_errada)
    assert r.status_code == 422


def test_campo_faltando(client):
    sem_temp = EXEMPLO.copy()
    del sem_temp["temp"]
    # TODO: mande o sem_temp e confira o código de erro
    r = client.post("/predict", json=sem_temp)
    assert r.status_code == 422


def test_contrato_com_o_treino():
    """A API e o treino precisam concordar sobre as entradas (nomes e ordem)."""
    # list(main.Hora.model_fields): os campos da classe Hora, na ordem em que foram escritos
    # FEATURES: as colunas que o treino usa (src/bike.py)
    assert list(main.Hora.model_fields) == FEATURES
