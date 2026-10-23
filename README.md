# TaskTracker

Sistema de gerenciamento de tarefas em linha de comando (CLI), desenvolvido em Python 3 como parte do **Bootcamp II** (Engenharia de Software, Versionamento de Código e Desenvolvimento de Sistemas).

> **Fase atual:** Fase 3 — Entrega Final (conteinerização com Docker, orquestração com Docker Compose e deploy).

## Autor

- **Nome:** Rafael Afonso Labarrère
- **Curso:** Ciências da Computação
- **Polo:** Asa Norte
- **E-mail institucional:** rafael.labarrere@sempreceub.com

## Descrição

No dia a dia pessoal e profissional, a falta de um método estruturado para controlar tarefas leva à desorganização, ao esquecimento de compromissos e à perda de prazos. O **TaskTracker** funciona como um organizador centralizado, permitindo cadastrar tarefas com prioridade e prazo e visualizá-las de forma clara no terminal.

## Funcionalidades

- **Cadastrar nova tarefa**, informando título, descrição, prioridade e data limite.
- **Visualizar tarefas cadastradas**, com todas as propriedades organizadas e legíveis.
- **Sair da aplicação.**

O menu é contínuo: o programa só encerra quando o usuário escolhe a opção de sair.

## Estrutura de Dados

Cada tarefa é representada por um dicionário Python:

| Campo         | Tipo   | Regra                                                      |
|---------------|--------|------------------------------------------------------------|
| `id`          | int    | Gerado automaticamente (incremental e único)               |
| `titulo`      | string | Obrigatório; não aceita vazio nem apenas espaços           |
| `descricao`   | string | Texto livre                                                |
| `prioridade`  | string | Apenas `Alta`, `Média` (ou `Media`) e `Baixa`              |
| `data_limite` | string | Prazo de conclusão (formato sugerido: `DD/MM/AAAA`)        |
| `status`      | string | Definido automaticamente como `Pendente` no cadastro       |

## Regras de Negócio

1. **Obrigatoriedade de título:** títulos vazios ou compostos só por espaços são rejeitados, e o sistema pede nova digitação até receber um título válido.
2. **Restrição de prioridade:** apenas `Alta`, `Média`/`Media` e `Baixa` são aceitas (também é possível digitar `1`, `2` ou `3`, sem diferenciar maiúsculas de minúsculas). Qualquer outro valor gera mensagem de erro e repete a pergunta.
3. **Identificação única:** cada tarefa recebe um ID incremental automaticamente.
4. **Status inicial:** toda tarefa nasce como `Pendente`.
5. **Lista vazia:** se não houver tarefas, o sistema informa que não existem registros no momento.

## Tecnologias Utilizadas

- [Python 3](https://www.python.org/) (somente biblioteca padrão)
- Git e GitHub para versionamento
- [Docker](https://www.docker.com/) e Docker Compose para conteinerização e orquestração

## Estrutura do Repositório

```
Bootcamp2/
├── README.md                      # Documentação principal e instruções de uso
├── .gitignore                     # Ignora arquivos temporários do Python e ambiente virtual
├── docs/
│   └── planejamento_logico.pdf    # Planejamento lógico e arquitetural (Fase 1)
├── src/
│   └── main.py                    # Código-fonte principal da aplicação (Fase 2)
├── Dockerfile                     # Receita da imagem Docker (Fase 3)
└── docker-compose.yml             # Orquestração da execução interativa (Fase 3)
```

## Instalação e Execução

**Pré-requisito:** Python 3.8 ou superior instalado.

```bash
# 1. Clone o repositório
git clone https://github.com/Rafael-Labarrere/Bootcamp2.git

# 2. Acesse a pasta do projeto
cd Bootcamp2

# 3. Execute a aplicação
python src/main.py
```

> Em alguns sistemas (Linux/macOS), use `python3 src/main.py`.

## Execução com Docker (Fase 3)

**Pré-requisito:** [Docker](https://docs.docker.com/get-docker/) instalado e em execução (o Docker Compose já vem incluído nas versões atuais).

```bash
# 1. Clone o repositório e acesse a pasta
git clone https://github.com/Rafael-Labarrere/Bootcamp2.git
cd Bootcamp2
```

**Como construir a imagem:**

```bash
docker build -t tasktracker-app .
```

**Como rodar o container em modo isolado:**

```bash
docker run -it tasktracker-app
```

**Como rodar via orquestração (Recomendado):**

```bash
docker compose run --rm tasktracker
```

### Por que `-it`, `stdin_open` e `tty`?

O TaskTracker é uma CLI interativa que usa `input()`. Por padrão, um container é isolado e não recebe entrada do teclado. Por isso:

- `-it` (no `docker run`) ou `stdin_open: true` + `tty: true` (no `docker-compose.yml`) mantêm a entrada de dados aberta e alocam um terminal virtual.
- `ENV PYTHONUNBUFFERED=1` no `Dockerfile` garante que as mensagens apareçam imediatamente no terminal, sem buffer.

### Dockerfile vs. docker-compose.yml

| | `Dockerfile` (a receita) | `docker-compose.yml` (o maestro) |
|---|---|---|
| **Papel** | Empacota a aplicação e suas dependências | Orquestra a execução interativa da CLI |
| **Saída** | Gera a imagem | Roda o container com os parâmetros necessários |
| **Comando-chave** | `docker build` | `docker compose run` |

> Os dados das tarefas ficam apenas em memória: ao encerrar o container (opção 3), a lista é perdida.

## Exemplo de Uso

```
===== TASKTRACKER =====
1. Cadastrar nova tarefa
2. Visualizar tarefas cadastradas
3. Sair
Escolha uma opção: 1

--- CADASTRO DE NOVA TAREFA ---
Título: 
O título não pode estar vazio.
Título: Elaborar relatório de vendas
Descrição: Consolidar planilhas do 3º trimestre em PDF
Prioridade (1. Alta/2. Média/3. Baixa): Urgente
Opção inválida. Escolha 1, 2 ou 3.
Prioridade (1. Alta/2. Média/3. Baixa): Alta
Data limite (DD/MM/AAAA): 30/10/2026
Tarefa 'Elaborar relatório de vendas' cadastrada com sucesso!

===== TASKTRACKER =====
1. Cadastrar nova tarefa
2. Visualizar tarefas cadastradas
3. Sair
Escolha uma opção: 2

--- LISTA DE TAREFAS ---
ID: 1
Título: Elaborar relatório de vendas
Descrição: Consolidar planilhas do 3º trimestre em PDF
Prioridade: Alta
Data limite: 30/10/2026
Status: Pendente
------------------------------
```

## Roadmap do Bootcamp II

- [x] **Fase 1:** Planejamento lógico, decomposição do problema e algoritmo em português.
- [x] **Fase 2:** Estruturação do repositório, versionamento com Git/GitHub e implementação em Python.
- [x] **Fase 3:** Empacotamento, containerização com Docker, orquestração com Docker Compose e deploy.

## Versionamento

O histórico de commits acompanha a evolução do projeto:

1. Commit inicial: `README.md`, `.gitignore` e documento da Fase 1.
2. Estrutura principal em `src/main.py` (menu e loop principal).
3. Funções de validação (título não vazio e prioridades).
4. Publicação remota no GitHub (`origin main`).

O desenvolvimento do código foi feito na branch `feature/menu-principal` e depois mesclado na `main`.