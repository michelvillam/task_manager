import json

from task_manager.Task import Task


class TaskManager:

    FILE_NAME = "tasks.json"

    def __init__(self):
        self.tasks = []
        self.next_id = 1

    def add_task(self, name, description):  
        task = Task(self.next_id, name, description)
        self.tasks.append(task)
        self.next_id += 1   
        self.save_tasks()  # Save tasks after adding a new task
        print(f"Task '{name}' added successfully.")

    def delete_task(self, id):
        for task in self.tasks:
            if task.id == id:
                self.tasks.remove(task)
                self.save_tasks()
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
                self.save_tasks()
                return
        print(f"No task found with ID {id}.")

    def load_tasks(self):
        try:
            with open(self.FILE_NAME, "r") as file:
                tasks_data = json.load(file)
                for task_data in tasks_data:

                    task = Task(task_data["id"], task_data["name"], task_data["description"], task_data["completed"])
                    self.tasks.append(task)
                    self.next_id = max(self.next_id, task.id + 1)
        except FileNotFoundError:
            self.tasks = []

    def save_tasks(self):
        tasks_data = [{"id": task.id, "name": task.name, "description": task.description, "completed": task.completed} for task in self.tasks]
        with open(self.FILE_NAME, "w") as file:
            json.dump(tasks_data, file, indent=4)
        

    