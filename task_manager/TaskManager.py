from task_manager.Task import Task


class TaskManager:
    def __init__(self):
        self.tasks = []
        self.next_id = 1

    def add_task(self, name, description):  
        task = Task(self.next_id, name, description)
        self.tasks.append(task)
        self.next_id += 1   
        print(f"Task '{name}' added successfully.")

    def delete_task(self, id):
        for task in self.tasks:
            if task.id == id:
                self.tasks.remove(task)
                print(f"Task '{task.name}' deleted successfully.")
                return  
        print(f"No task found with ID {id}.")

    def get_tasks(self):
        if not self.tasks:
            print("No tasks available.")
        else:
            for task in self.tasks:
                print(task)

    def mark_task_completed(self, id):
        for task in self.tasks:
            if task.id == id:
                task.mark_completed()
                print(f"Task '{task.name}' marked as completed.")
                return
        print(f"No task found with ID {id}.")
        

    