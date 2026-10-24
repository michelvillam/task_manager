from task_manager.TaskManager import TaskManager

def print_menu():
    print("\nTask Manager")
    print("1. Add Task")
    print("2. Delete Task")
    print("3. View Tasks")
    print("4. Mark Task as Completed")
    print("5. Exit")

def main():
    task_manager = TaskManager()
    task_manager.load_tasks()
    while True:
        print_menu()

        try:
            choice = int(input("Enter your choice: "))
                    
            match choice:
                case 1:
                    name = input("Enter task name: ")
                    description = input("Enter task description: ")
                    task_manager.add_task(name, description)
                case 2:
                    id = int(input("Enter task ID to delete: "))
                    task_manager.delete_task(id)
                case 3:
                    task_manager.get_tasks()
                case 4:
                    id = int(input("Enter task ID to mark as completed: "))
                    task_manager.mark_task_completed(id)
                case 5:
                    break
                case _:
                    print("Invalid choice. Please try again.")


        except ValueError:
            print("Invalid input. Please enter a number.")
            print_menu
        


if __name__ == "__main__":
    main()  