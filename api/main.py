"""API de previsão de demanda de bicicletas.

Rode da raiz do repositório:
    uvicorn api.main:app --port 8000 --reload
"""
from contextlib import asynccontextmanager

import mlflow
import pandas as pd
from dotenv import load_dotenv
from fastapi import FastAPI
from mlflow import MlflowClient
from pydantic import BaseModel, Field

# Endereço e credenciais do MLflow (DagsHub). No Codespace vêm do .env, que vale mais que o padrão
# do devcontainer. No Docker e no GitHub Actions não há .env: vêm das variáveis de ambiente.
load_dotenv(override=True)

MODEL_NAME = "bike-demand"
estado = {}  # o modelo carregado e a versão dele

class Hora(BaseModel):
    """As 12 entradas do modelo para uma hora do dia."""
    season: int = Field(ge=1, le=4, description="estação do ano (1 a 4)")
    yr: int = Field(ge=0, le=1, description="ano (0 = 2011, 1 = 2012)")
    # TODO: troque os ... pelos limites (ge=..., le=...) de cada campo, como nos dois de cima
    mnth: int = Field(ge=1, le=12, description="mês")
    hr: int = Field(ge=0, le=23, description="hora do dia")
    holiday: int = Field(ge=0, le=1, description="feriado (0 ou 1)")
    weekday: int = Field(ge=0, le=6, description="dia da semana (0 = domingo)")
    workingday: int = Field(ge=0, le=1, description="dia útil (0 ou 1)")
    weathersit: int = Field(ge=1, le=4, description="clima (1 = limpo ... 4 = chuva forte)")
    temp: float = Field(ge=0, le=1, description="temperatura normalizada")
    atemp: float = Field(ge=0, le=1, description="sensação térmica normalizada")
    hum: float = Field(ge=0, le=1, description="umidade normalizada")
    windspeed: float = Field(ge=0, le=1, description="velocidade do vento normalizada")

class Previsao(BaseModel):
    cnt: int = Field(description="aluguéis previstos para a hora")
    model_version: str = Field(description="versão do modelo que respondeu")


def carregar_modelo():
    """O consumidor da T3 da Aula 1: só conhece o alias @champion.

    O endereço e as credenciais do MLflow vêm das variáveis de ambiente MLFLOW_TRACKING_*.
    """
    versao = MlflowClient().get_model_version_by_alias(MODEL_NAME, "champion").version
    modelo = mlflow.pyfunc.load_model(f"models:/{MODEL_NAME}/{versao}")
    return modelo, versao


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Roda uma vez, quando a API sobe: carregar o modelo a cada requisição seria lento.
    estado["modelo"], estado["versao"] = carregar_modelo()
    yield


app = FastAPI(title="Bike Demand API", lifespan=lifespan)


@app.get("/health")
def health():
    return {"status": "ok", "model": MODEL_NAME, "model_version": estado["versao"]}


@app.post("/predict")
def predict(hora: Hora) -> Previsao:
    X = pd.DataFrame([hora.model_dump()]).astype("float64")
    cnt = float(estado["modelo"].predict(X)[0])
    # Regra de negócio: aluguel não é negativo nem fracionado.
    return Previsao(cnt=max(0, round(cnt)), model_version=estado["versao"])
