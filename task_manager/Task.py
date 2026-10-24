class Task:
    def __init__(self, id, name, description, completed=False):
        self.id = id
        self.name = name
        self.description = description
        self.completed = completed

    def mark_completed(self):
        self.completed = True

    def __str__(self):
        status = "Completed" if self.completed else "Pending"
        return f"Task: {self.name}\nDescription: {self.description}\nStatus: {status}"