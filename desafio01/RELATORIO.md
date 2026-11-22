# Desafio 1: relatório

**Aluno(a):**

## 1. Versões dos dados

Rode o comando abaixo e complete a tabela com os 8 primeiros caracteres de cada md5:

```bash
for tag in dados-v1 dados-v2 dados-v3; do
  echo "$tag $(git show $tag:data/raw/bike.csv.dvc | awk '/md5/{print $3}')"
done
```

| Tag | md5 (8 primeiros caracteres) | Período |
|---|---|---|
| `dados-v1` | `fc7d423a` | 01/01/2011 a 31/12/2011 |
| `dados-v2` | | 01/01/2011 a 30/06/2012 |
| `dados-v3` | | 01/01/2011 a 31/12/2012 |

## 2. Comparação no mesmo teste

Copie os números de `reports/comparacao.json`.

**Período do teste:** 2012-12-04 a 2012-12-31 (670 linhas)

| Alias | Versão | RMSE | MAE | R² |
|---|---|---|---|---|
| `@champion` |6|92.19176001086102|64.13851732327079|0.6728782248198821|
| `@challenger` |6|62.89373227496592|41.50570554415892|0.8477560730724738|


## 3. Decisão

**Promovido ou rejeitado?**

comando: dvc repro

            versao    rmse     mae     r2
champion       4.0  92.192  64.139  0.673

challenger     6.0  62.894  41.506  0.848


Teste: 2012-12-04 a 2012-12-31 (670 linhas)

Challenger VENCEU: RMSE 62.9 vs 92.2 (champion)

✅ Promovido: champion -> versão 6 (anterior: 4)


**Justificativa (2 a 3 frases):**

## 4. O que cada ferramenta fez nesse projeto?

**Pergunta 01:**
Com suas palavras, quais os dois usos do DVC nesse projeto?

1. **Versionar dados e arquivos grandes:** Como o Git não é feito para guardar bases de dados pesadas (`bike.csv`) nem modelos treinados, o DVC guarda esses arquivos em um armazenamento separado e cria pequenos arquivos `.dvc` para controlar cada versão junto com o Git (`dados-v1`, `dados-v2`, `dados-v3`).
2. **Automatizar o pipeline de treino (`dvc.yaml` e `dvc repro`):** Ele organiza a ordem das etapas do projeto (preparar dados, dividir, treinar, avaliar e comparar) e roda automaticamente apenas o que precisa ser atualizado quando algum dado ou código muda.

**Pergunta 02:**
Com suas palavras, para que serve o MLflow nesse projeto?

O MLflow funciona como um histórico e gerenciador oficial dos modelos. Ele registra os resultados de cada treino (métricas como RMSE e MAE), guarda todas as versões do modelo criadas e controla quem é o modelo oficial em produção (`@champion`) e quem está sendo testado para substituí-lo (`@challenger`), registrando o motivo da aprovação ou rejeição.