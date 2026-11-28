#!/usr/bin/env bash
# Deixa o repositório no ponto de partida da Aula 2:
# DVC inicializado, pipeline com os 5 estágios da T1 e dados v3 (2012 completo) versionados.
# Pode rodar mais de uma vez: cada passo só age se estiver faltando.
#
#   bash scripts/recuperar_aula01.sh
set -e
cd "$(git rev-parse --show-toplevel)"

echo "1/4 DVC"
if [ ! -d .dvc ]; then
  dvc init -q
  git add .dvc .dvcignore
  git commit -qm "Inicializa DVC"
  echo "    DVC inicializado"
else
  echo "    ok"
fi

echo "2/4 Pipeline (dvc.yaml)"
if ! grep -q "evaluate:" dvc.yaml 2>/dev/null || ! grep -q "plot:" dvc.yaml 2>/dev/null; then
  cat > dvc.yaml <<'YAML'
# Pipeline do projeto. Cada estágio declara o comando (cmd), o que ele lê (deps),
# os parâmetros do params.yaml que usa (params) e o que ele gera (outs).
stages:
  prepare:
    cmd: python src/prepare.py
    deps:
    - src/prepare.py
    - src/bike.py
    - data/raw/bike.csv
    outs:
    - data/prepared

  split:
    cmd: python src/split.py
    deps:
    - src/split.py
    - src/bike.py
    - data/prepared
    params:
    - split
    outs:
    - data/split

  train:
    cmd: python src/train.py
    deps:
    - src/train.py
    - src/bike.py
    - data/split/train.csv
    params:
    - train
    - mlflow
    outs:
    - models

  evaluate:
    cmd: python src/evaluate.py
    deps:
    - src/evaluate.py
    - src/bike.py
    - models
    - data/split/test.csv
    metrics:
    - metrics.json:
        cache: false

  plot:
    cmd: python src/plot.py
    deps:
    - src/plot.py
    - src/bike.py
    - models
    - data/split/test.csv
    plots:
    - reports/previsto_vs_real.png:
        cache: false
YAML
  git add dvc.yaml
  git commit -qm "Pipeline DVC com 5 estágios"
  echo "    dvc.yaml gravado com os 5 estágios da T1"
else
  echo "    ok"
fi

echo "3/4 Dados v3 (2012 completo)"
ULTIMA=$(tail -n 1 data/raw/bike.csv 2>/dev/null | cut -d, -f2 || true)
if [ "$ULTIMA" != "2012-12-31" ]; then
  python src/get_data.py --until 2012-12-31
else
  echo "    ok"
fi

echo "4/4 Versão dos dados no DVC"
git rm -q --cached data/raw/bike.csv 2>/dev/null || true   # o dado não fica no Git
dvc add -q data/raw/bike.csv 2>/dev/null
git add data/raw/bike.csv.dvc
if [ -f data/raw/.gitignore ]; then   # o DVC só cria este arquivo quando o CSV ainda não está ignorado
  git add data/raw/.gitignore
fi
if ! git diff --cached --quiet; then
  git commit -qm "Dados v3: 2012 completo"
  echo "    dados v3 versionados"
else
  echo "    ok"
fi
git tag dados-v3 2>/dev/null || true

echo
echo "Pronto. Dados: $(wc -l < data/raw/bike.csv) linhas | md5 $(awk '/md5/{print $3}' data/raw/bike.csv.dvc | cut -c1-8)"
