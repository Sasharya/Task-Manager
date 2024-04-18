import pandas as pd
from colorama import init, Fore, Style
import re

init()

tasks = pd.DataFrame(columns=["Nome da Tarefa", "Descrição", "Data de Entrega", "Prioridade", "Status"])

def add_task(task_name, description, due_date, priority):
    if not task_name or not re.match(r'^[a-zA-Z0-9\s]+$', task_name):
        print(Fore.RED + "Nome da tarefa inválido. Por favor, use apenas letras, números e espaços." + Style.RESET_ALL)
        return
    if not description or not re.match(r'^[a-zA-Z0-9\s.,!?]+$', description):
        print(Fore.RED + "Descrição inválida. Por favor, use apenas letras, números, espaços e os seguintes caracteres: .,!?" + Style.RESET_ALL)
        return
    try:
        due_date = pd.to_datetime(due_date)
    except ValueError:
        print(Fore.RED + "Data de entrega inválida. Por favor, use AAAA-MM-DD." + Style.RESET_ALL)
        return
    if not re.match(r'^\d+$', priority):
        print(Fore.RED + "Prioridade inválida. Por favor, use apenas números." + Style.RESET_ALL)
        return
    new_task = {"Nome da Tarefa": task_name, "Descrição": description, "Data de Entrega": due_date, "Prioridade": priority, "Status": "Não iniciada"}
    global tasks
    tasks = tasks._append(new_task, ignore_index=True)
    print(Fore.GREEN + f"Tarefa '{task_name}' adicionada." + Style.RESET_ALL)

def view_tasks():
    global tasks
    if tasks.empty:
        print("Nenhuma tarefa encontrada.")
    else:
        sort_by = input("Como gostaria de organizar as tarefas? (Data de entrega, prioridade, status, ou pressione enter para seguir): ")
        sorted_tasks = tasks.copy()
        if sort_by == "Data de Entrega":
            sorted_tasks = sorted_tasks.sort_values(by=["Data de Entrega"])
        elif sort_by == "Prioridade":
            sorted_tasks = sorted_tasks.sort_values(by=["Prioridade"])
        elif sort_by == "status":
            sorted_tasks = sorted_tasks.sort_values(by=["Status"])
        else:
            sorted_tasks = tasks.sort_index()

        print("\n" + Fore.CYAN + "Lista de Tarefas" + Style.RESET_ALL)
        for index, row in sorted_tasks.iterrows():
            status_color = Fore.GREEN if row["Status"] == "Completa" else Fore.YELLOW if row["Status"] == "Em Progresso" else Fore.RED
            print(f"  {index + 1}. {row['Nome da Tarefa']} - Status: {status_color}{row['Status']}, Descrição: {row['Descrição']}, Data de Entrega: {row['Data de Entrega']}, Prioridade: {row['Prioridade']}" + Style.RESET_ALL)

def update_task_status(task_id, status):
    if not re.match(r'^\d+$', task_id):
        print(Fore.RED + "ID da tarefa inválido. Por favor, use apenas números." + Style.RESET_ALL)
        return
    if int(task_id) < 1 or int(task_id) > len(tasks):
        print(Fore.RED + "Tarefa não encontrada." + Style.RESET_ALL)
        return
    tasks.loc[int(task_id) - 1, "Status"] = status
    print(Fore.GREEN + f"Tarefa {task_id} foi modificada para {status}." + Style.RESET_ALL)

def delete_task(task_id):
    global tasks
    if not re.match(r'^\d+$', task_id):
        print(Fore.RED + "ID da tarefa inválido. Por favor, use apenas números." + Style.RESET_ALL)
        return
    if int(task_id) < 1 or int(task_id) > len(tasks):
        print(Fore.RED + "Tarefa não encontrada." + Style.RESET_ALL)
        return
    tasks = tasks.drop(int(task_id) - 1)
    tasks = tasks.reset_index(drop=True)
    print(Fore.GREEN + f"Tarefa {task_id} deletada." + Style.RESET_ALL)

def main():
    while True:
        print("\n" + Fore.CYAN + "Gerenciador de Tarefas" + Style.RESET_ALL)
        print("1. Adicionar tarefa")
        print("2. Ver Tarefas")
        print("3. Marcar Tarefa como Completa")
        print("4. Marcar Tarefa como Em Progresso")
        print("5. Deletar Tarefa")
        print("6. Sair")

        choice = input(Fore.YELLOW + "Digite sua opção: " + Style.RESET_ALL)

        if choice == "1":
            task_name = input("Coloque a ID (nome) da tarefa: ")
            description = input("Coloque a descrição da tarefa: ")
            due_date = input("Coloque a data de entrega (YYYY-MM-DD): ")
            priority = input("Coloque o número que define a prioridade dessa tarefa (a partir de 1): ")
            add_task(task_name, description, due_date, priority)
        elif choice == "2":
            view_tasks()
        elif choice == "3":
            task_id = input("Digite a ID da tarefa que você quer marcar como Completa: ")
            update_task_status(task_id, "Completa")
        elif choice == "4":
            task_id = input("Digite a ID da tarefa que você quer marcar como Em Progresso: ")
            update_task_status(task_id, "Em Progresso")
        elif choice == "5":
            task_id = input("Digite a ID da tarefa que você quer deletar: ")
            delete_task(task_id)
        elif choice == "6":
            print("Tchau... Até a próxima :)")
            break
        else:
            print(Fore.RED + "Escolha inválica. Por favor, tente novamente." + Style.RESET_ALL)

if __name__ == "__main__":
    main()
