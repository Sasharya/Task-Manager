import pandas as pd # type: ignore
from colorama import init, Fore, Style
import re

init()

tasks = pd.DataFrame(columns=["Task Name", "Description", "Due Date", "Priority", "Status"])

def add_task(task_name, description, due_date, priority):
    if not task_name or not re.match(r'^[a-zA-Z0-9\s]+$', task_name):
        print(Fore.RED + "Invalid task name. Please only use letters, numbers, and spaces." + Style.RESET_ALL)
        return
    if not description or not re.match(r'^[a-zA-Z0-9\s.,!?]+$', description):
        print(Fore.RED + "Invalid description. Please only use letters, numbers, spaces, and the following characters: .,!?" + Style.RESET_ALL)
        return
    try:
        due_date = pd.to_datetime(due_date)
    except ValueError:
        print(Fore.RED + "Invalid due date format. Please use YYYY-MM-DD." + Style.RESET_ALL)
        return
    if not re.match(r'^\d+$', priority):
        print(Fore.RED + "Invalid priority. Please only use numbers." + Style.RESET_ALL)
        return
    new_task = {"Task Name": task_name, "Description": description, "Due Date": due_date, "Priority": priority, "Status": "Not Started"}
    global tasks
    tasks = tasks._append(new_task, ignore_index=True)
    print(Fore.GREEN + f"Task '{task_name}' added." + Style.RESET_ALL)

def view_tasks():
    global tasks
    if tasks.empty:
        print("No tasks.")
    else:
        sort_by = input("How would you like to sort the tasks? (due date, priority, status, or press enter to skip sorting): ")
        sorted_tasks = tasks.copy()
        if sort_by == "due date":
            sorted_tasks = sorted_tasks.sort_values(by=["Due Date"])
        elif sort_by == "priority":
            sorted_tasks = sorted_tasks.sort_values(by=["Priority"])
        elif sort_by == "status":
            sorted_tasks = sorted_tasks.sort_values(by=["Status"])
        else:
            sorted_tasks = tasks.sort_index()

        print("\n" + Fore.CYAN + "Task List" + Style.RESET_ALL)
        for index, row in sorted_tasks.iterrows():
            status_color = Fore.GREEN if row["Status"] == "Completed" else Fore.YELLOW if row["Status"] == "In Progress" else Fore.RED
            print(f"  {index + 1}. {row['Task Name']} - Status: {status_color}{row['Status']}, Description: {row['Description']}, Due Date: {row['Due Date']}, Priority: {row['Priority']}" + Style.RESET_ALL)

def update_task_status(task_id, status):
    if not re.match(r'^\d+$', task_id):
        print(Fore.RED + "Invalid task ID. Please only use numbers." + Style.RESET_ALL)
        return
    if int(task_id) < 1 or int(task_id) > len(tasks):
        print(Fore.RED + "Task not found." + Style.RESET_ALL)
        return
    tasks.loc[int(task_id) - 1, "Status"] = status
    print(Fore.GREEN + f"Task {task_id} status updated to {status}." + Style.RESET_ALL)

def delete_task(task_id):
    if not re.match(r'^\d+$', task_id):
        print(Fore.RED + "Invalid task ID. Please only use numbers." + Style.RESET_ALL)
        return
    if int(task_id) < 1 or int(task_id) > len(tasks):
        print(Fore.RED + "Task not found." + Style.RESET_ALL)
        return
    tasks = tasks.drop(int(task_id) - 1)
    tasks = tasks.reset_index(drop=True)
    print(Fore.GREEN + f"Task {task_id} deleted." + Style.RESET_ALL)

def main():
    while True:
        print("\n" + Fore.CYAN + "Task Manager" + Style.RESET_ALL)
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Mark Task as Completed")
        print("4. Mark Task as In Progress")
        print("5. Delete Task")
        print("6. Exit")

        choice = input(Fore.YELLOW + "Enter your choice: " + Style.RESET_ALL)

        if choice == "1":
            task_name = input("Enter task name: ")
            description = input("Enter task description: ")
            due_date = input("Enter due date (YYYY-MM-DD): ")
            priority = input("Enter priority: ")
            add_task(task_name, description, due_date, priority)
        elif choice == "2":
            view_tasks()
        elif choice == "3":
            task_id = input("Enter task ID to mark as completed: ")
            update_task_status(task_id, "Completed")
        elif choice == "4":
            task_id = input("Enter task ID to mark as in progress: ")
            update_task_status(task_id, "In Progress")
        elif choice == "5":
            task_id = input("Enter task ID to delete: ")
            delete_task(task_id)
        elif choice == "6":
            print("Exiting...")
            break
        else:
            print(Fore.RED + "Invalid choice. Please try again." + Style.RESET_ALL)

if __name__ == "__main__":
    main()