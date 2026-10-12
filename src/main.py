"""TaskTracker - Gerenciador de tarefas em linha de comando.

Parte 2: Validação de dados e melhorias na interface.

"""

# Lista principal: guarda todas as tarefas (cada tarefa é um dicionário)
tarefas = []

# Contador para gerar IDs incrementais e únicos
proximo_id = 1


def exibir_menu():
    #Mostra as opções do menu principal.
    print("\n===== TASKTRACKER =====")
    print("1. Cadastrar nova tarefa")
    print("2. Visualizar tarefas cadastradas")
    print("3. Sair")


def cadastrar_tarefa():
    #Pede os dados da tarefa e salva na lista.
    global proximo_id

    dsasasd
    print("\n--- CADASTRO DE NOVA TAREFA ---")
    while True:    
        titulo = input("Título: ")
        if titulo.strip():
            break
        print("O título não pode estar vazio.")

    descricao = input("Descrição: ")

    while True:
        prioridade = input("Prioridade (Alta/Média/Baixa): ")
        if prioridade in ["Alta", "Média", "Baixa"]:
            break
        print("Prioridade inválida. Escolha entre Alta, Média ou Baixa.")

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