# Imagem base: Python 3.12 em um Linux enxuto
FROM python:3.12-slim

WORKDIR /app

# 1) Dependências primeiro: esta camada só é refeita quando o requirements-api.txt muda
COPY requirements-api.txt .
RUN pip install --no-cache-dir -r requirements-api.txt

# 2) Código da API por último: é o que mais muda
COPY api/ api/

EXPOSE 8000
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
