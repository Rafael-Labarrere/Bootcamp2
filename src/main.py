"""TaskTracker - Gerenciador de tarefas em linha de comando.

Parte 2: Validação de dados e melhorias na interface.

"""

import json
import os

# Arquivo onde as tarefas são salvas (fica em data/tarefas.json, na raiz do projeto,
# independente da pasta de onde o programa for executado)
PASTA_DADOS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
ARQUIVO_TAREFAS = os.path.join(PASTA_DADOS, "tarefas.json")

# Lista principal: guarda todas as tarefas (cada tarefa é um dicionário)
tarefas = []

# Contador para gerar IDs incrementais e únicos
proximo_id = 1


def carregar_tarefas():
    #Lê as tarefas do arquivo JSON (se existir) e atualiza o próximo ID.
    global tarefas, proximo_id

    if not os.path.exists(ARQUIVO_TAREFAS):
        return  # primeira execução: começa vazio

    try:
        with open(ARQUIVO_TAREFAS, "r", encoding="utf-8") as arquivo:
            tarefas = json.load(arquivo)
    except (json.JSONDecodeError, OSError):
        print("Aviso: não foi possível ler o arquivo de tarefas. Iniciando com lista vazia.")
        tarefas = []
        return

    # Continua a numeração a partir do maior ID já existente
    proximo_id = max((t["id"] for t in tarefas), default=0) + 1


def salvar_tarefas():
    #Grava a lista de tarefas no arquivo JSON.
    os.makedirs(PASTA_DADOS, exist_ok=True)
    caminho_temp = ARQUIVO_TAREFAS + ".tmp"

    # Escreve num arquivo temporário e depois substitui, evitando corromper
    # o arquivo original caso o programa seja interrompido durante a gravação
    with open(caminho_temp, "w", encoding="utf-8") as arquivo:
        json.dump(tarefas, arquivo, ensure_ascii=False, indent=2)
    os.replace(caminho_temp, ARQUIVO_TAREFAS)


def exibir_menu():
    #Mostra as opções do menu principal.
    print("\n===== TASKTRACKER =====")
    print("1. Cadastrar nova tarefa")
    print("2. Visualizar tarefas cadastradas")
    print("3. Sair")


def cadastrar_tarefa():
    #Pede os dados da tarefa e salva na lista.
    global proximo_id

    # Validação do título: não pode ser vazio
    print("\n--- CADASTRO DE NOVA TAREFA ---")
    while True:    
        titulo = input("Título: ")
        if titulo.strip():
            break
        print("O título não pode estar vazio.")

    #Descrição pode ser vazia
    descricao = input("Descrição: ")

    # Validação da prioridade: deve ser Alta, Média ou Baixa
    while True:
        prioridade = input("Prioridade (1. Alta/2. Média/3. Baixa): ").strip().capitalize()
        if prioridade == "1" or prioridade == "Alta":
            prioridade = "Alta"
        elif prioridade == "2" or prioridade == "Média" or prioridade == "Media":
            prioridade = "Média"
        elif prioridade == "3" or prioridade == "Baixa":
            prioridade = "Baixa"
        else:
            print("Opção inválida. Escolha 1, 2 ou 3.")
            continue
        break

    #Data limite sem validação
    data_limite = input("Data limite (DD/MM/AAAA): ")

    tarefa = {
        "id": proximo_id,
        "titulo": titulo,
        "descricao": descricao,
        "prioridade": prioridade,
        "data_limite": data_limite,
        "status": "Pendente",  # todo cadastro começa como Pendente
    }

    tarefas.append(tarefa)
    proximo_id += 1  # o próximo cadastro terá um ID novo
    salvar_tarefas()  # persiste imediatamente em disco

    print(f"Tarefa '{titulo}' cadastrada com sucesso!")


def visualizar_tarefas():
    #Lista todas as tarefas ou avisa que não há nenhuma.
    print("\n--- LISTA DE TAREFAS ---")

    if len(tarefas) == 0:
        print("Nenhuma tarefa cadastrada até o momento.")
        return

    for tarefa in tarefas:
        print(f"ID: {tarefa['id']}")
        print(f"Título: {tarefa['titulo']}")
        print(f"Descrição: {tarefa['descricao']}")
        print(f"Prioridade: {tarefa['prioridade']}")
        print(f"Data limite: {tarefa['data_limite']}")
        print(f"Status: {tarefa['status']}")
        print("-" * 30)


def main():
    #Loop principal: repete o menu até o usuário escolher sair.
    carregar_tarefas()  # recupera as tarefas salvas em execuções anteriores
    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            cadastrar_tarefa()
        elif opcao == "2":
            visualizar_tarefas()
        elif opcao == "3":
            print("Encerrando o TaskTracker. Até logo!")
            break  # sai do loop e encerra o programa
        else:
            print("Opção inválida. Escolha 1, 2 ou 3.")


if __name__ == "__main__":
    main()