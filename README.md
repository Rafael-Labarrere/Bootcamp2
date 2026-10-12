TaskTracker

Sistema de gerenciamento de tarefas em linha de comando (CLI), desenvolvido em Python 3 como parte do Bootcamp II (Engenharia de Software, Versionamento de Código e Desenvolvimento de Sistemas).

Fase atual: Fase 2 — Entrega Intermediária (Git/GitHub, implementação em Python e validação das regras de negócio).

Sobre o Autor
Nome: Rafael Afonso Labarrère
Curso: Ciências da Computação
Polo: Asa Norte
E-mail institucional: rafael.labarrere@sempreceub.com
Descrição:

No dia a dia pessoal e profissional, a falta de um método estruturado para controlar tarefas leva à desorganização, ao esquecimento de compromissos e à perda de prazos. O TaskTracker funciona como um organizador centralizado, permitindo cadastrar tarefas com prioridade e prazo e visualizá-las de forma clara no terminal.

Funcionalidades
Cadastrar nova tarefa, informando título, descrição, prioridade e data limite.
Visualizar tarefas cadastradas, com todas as propriedades organizadas e legíveis.
Sair da aplicação.

O menu é contínuo: o programa só encerra quando o usuário escolhe a opção de sair.

Estrutura de Dados

Cada tarefa é representada por um dicionário Python:

Campo	Tipo	Regra
id	int	Gerado automaticamente (incremental e único)
titulo	string	Obrigatório; não aceita vazio nem apenas espaços
descricao	string	Texto livre
prioridade	string	Apenas Alta, Média (ou Media) e Baixa
data_limite	string	Prazo de conclusão (formato sugerido: DD/MM/AAAA)
status	string	Definido automaticamente como Pendente no cadastro
Regras de Negócio
Obrigatoriedade de título: títulos vazios ou compostos só por espaços são rejeitados, e o sistema pede nova digitação até receber um título válido.
Restrição de prioridade: apenas Alta, Média/Media e Baixa são aceitas. Qualquer outro valor gera mensagem de erro e repete a pergunta.
Identificação única: cada tarefa recebe um ID incremental automaticamente.
Status inicial: toda tarefa nasce como Pendente.
Lista vazia: se não houver tarefas, o sistema informa que não existem registros no momento.
Tecnologias Utilizadas
Python 3 (somente biblioteca padrão)
Git e GitHub para versionamento
Estrutura do Repositório
tasktracker-projeto/
├── README.md                      # Documentação principal e instruções de uso
├── .gitignore                     # Ignora arquivos temporários do Python e ambiente virtual
├── docs/
│   └── planejamento_logico.pdf    # Planejamento lógico e arquitetural (Fase 1)
└── src/
    └── main.py                    # Código-fonte principal da aplicação
Instalação e Execução

Pré-requisito: Python 3.8 ou superior instalado.

bash
# 1. Clone o repositório
git clone https://github.com/Rafael-Labarrere/Bootcamp2.git

# 2. Acesse a pasta do projeto
cd Bootcamp2

# 3. Execute a aplicação
python src/main.py

Em alguns sistemas (Linux/macOS), use python3 src/main.py.

Exemplo de Uso
===== TASKTRACKER =====
1. Cadastrar nova tarefa
2. Visualizar tarefas cadastradas
3. Sair
Escolha uma opção: 1

--- CADASTRO DE NOVA TAREFA ---
Título: 
O título é obrigatório. Por favor, digite um título válido.
Título: Elaborar relatório de vendas
Descrição: Consolidar planilhas do 3º trimestre em PDF
Prioridade (Alta/Média/Baixa): Urgente
Opção inválida. Escolha Alta, Média ou Baixa.
Prioridade (Alta/Média/Baixa): Alta
Data limite (DD/MM/AAAA): 30/10/2026
Tarefa 'Elaborar relatório de vendas' cadastrada com sucesso!
Roadmap do Bootcamp II
 Fase 1: Planejamento lógico, decomposição do problema e algoritmo em português.
 Fase 2: Estruturação do repositório, versionamento com Git/GitHub e implementação em Python (em andamento).
 Fase 3: Empacotamento, containerização com Docker, testes e deploy.
Versionamento

O histórico de commits acompanha a evolução do projeto:

Commit inicial: README.md, .gitignore e documento da Fase 1.
Estrutura principal em src/main.py (menu e loop principal).
Funções de validação (título não vazio e prioridades).
Publicação remota no GitHub (origin main).