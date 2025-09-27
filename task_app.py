import json
import os

DATA_FILE = os.path.join("data", "tasks.json")


class Task:
    def __init__(self, title, due_date=None, status="pending"):
        self.title = title
        self.due_date = due_date
        self.status = status # "pending", "done", "failed"

    def __repr__(self):
        due = f" (due {self.due_date})"
        if self.due_date else "" 
        return f"{self.title}{due} [{self.status}]"
