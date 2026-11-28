# Aula 2: deploy com FastAPI e Docker

Os notebooks das tarefas são liberados ao longo da aula. Arraste cada um para a pasta `aula02/` do seu Codespace
e faça as tarefas **na ordem**: cada uma usa o resultado da anterior.

| Tarefa | Tema |
|---|---|
| **T0** | DagsHub: remote do DVC e servidor MLflow fora do Codespace |
| **T1** | FastAPI: a API que serve o `@champion`, com validação e testes |
| **T2** | Docker: imagem e container da API; promover um modelo novo e voltar ao anterior com o container no ar |
| **T3** | GitHub Actions: testes, build, teste do container (smoke test) e publicação da imagem no GitHub Container Registry |

> **Antes de tudo:** arraste o `recuperar_aula01.sh` para a pasta `scripts/`. A T0 usa esse script para conferir
> o ponto de partida do seu repositório.

## Como cada tarefa funciona

Os notebooks de `t1_...` a `t3_...` têm duas partes:

1. **Parte 1 · Juntos:** alguém compartilha a tela e rodamos uma vez, conversando sobre cada passo.
2. **Parte 2 · Sozinhos:** você aplica o mesmo fluxo a um caso novo, no seu Codespace. As células com `# TODO` são suas.

A T0 é toda feita junto.

- Nas células `%%bash`, os comandos que mudam o Git, o DVC e o Docker vêm comentados (com `#`), para não rodarem
  sem querer. Quando chegar a hora, tire o `#` (selecione as linhas e use **Ctrl + /**) e rode a célula.
- As células `%%writefile` gravam o arquivo inteiro. Pode rodar de novo sem medo de duplicar nada.

## O que muda em relação à Aula 1

- O MLflow e o remote do DVC passam a ficar no **DagsHub**. O `scripts/start_mlflow.sh` não é mais necessário.
- As credenciais ficam no arquivo **`.env`**, que nunca vai para o Git. Os notebooks carregam o `.env` sozinhos.
  Em um terminal novo, carregue com `set -a; source .env; set +a`.
- O trabalho de hoje fica na branch **`aula_02`**, criada no passo 0 da T0. A `main` só recebe tudo no último
  passo da T3, por um *pull request*. O Desafio 2 é feito na `main`, depois desse merge.

## Problemas comuns

| Sintoma | Solução |
|---|---|
| `docker: command not found` | O Docker entrou no `devcontainer.json` do repositório da disciplina. No GitHub, no seu repositório: **Sync fork** → **Update branch**. No Codespace: `git switch main`, `git pull`, `git switch aula_02`, `git merge main` e depois **Ctrl + Shift + P** → **Codespaces: Rebuild Container**. O conteúdo do repositório é mantido. |
| O *pull request* abriu no repositório da disciplina | Feche esse PR e abra outro: no topo da página, troque o **base repository** para o seu repositório, com *base* `main` e *compare* `aula_02`. |
| `401` ou `403` ao falar com o DagsHub | Confira o `.env`: usuário, repositório e token, sem aspas e sem espaços. Rode de novo a célula que carrega o `.env`. |
| `dvc repro` ou `pytest` no terminal tentam usar `127.0.0.1:5000` | O terminal não carregou o `.env`: `set -a; source .env; set +a` |
| `address already in use` na porta 8000 | Há outro processo na porta: pare o `uvicorn` (**Ctrl + C**) ou o container (`docker stop bike-api`). |
| `docker run` reclama que o nome `bike-api` já existe | `docker rm -f bike-api` e rode de novo. |
| A API não sobe: `Application startup failed` ou fica parada em `Waiting for application startup` | Ela não achou o `@champion`. Confira o `.env` (sem aspas, na raiz do repositório) e, no MLflow do DagsHub, se o alias existe (T0, passo 7). |
| Depois do `git push`, a aba **Actions** não mostra nada | Em repositórios criados com *fork*, os workflows começam desativados. Aba **Actions** → **I understand my workflows, go ahead and enable them**. Depois, faça um novo push (sem mudança nenhuma: `git commit --allow-empty -m "Dispara o CI"` e `git push`). |
| O `git push` recusa o arquivo `.github/workflows/ci.yml` | Crie o arquivo pelo site: no GitHub, **Actions** → **set up a workflow yourself**, cole o conteúdo, **Commit changes**. No Codespace: `git pull`. |
| `docker pull` do GitHub Container Registry dá `denied` | No GitHub: **Packages** → a imagem → **Package settings** → **Change visibility** → **Public**. |

**Cota gratuita do Codespaces:** ao terminar, pare o Codespace (**Code → Codespaces → ⋯ → Stop codespace**).
O Docker consome mais disco: se faltar espaço, `docker system prune -f` remove o que não está em uso.
