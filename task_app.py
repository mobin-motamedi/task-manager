import json
import os
from datetime import datetime

DATA_FILE = os.path.join("data", "tasks.json")


class Task:
    def __init__(self, title, due_date=None, status="pending", created_at=None):
        self.title = title
        self.due_date = due_date
        self.status = status # "pending", "done", "failed"
        self.created_at = created_at or datetime.now().isoformat()


    def __repr__(self):
        due = f" (due {self.due_date})" if self.due_date else ""
        return f"[{self.id}] {self.title}{due} [{self.status}]"
    

class TaskManager:
    def __init__(self):
        self.tasks = []
        self.current_page = 0
        self.page_size = 5
        self.load_tasks()
    
    def load_tasks(self):
        """Load tasks from JSON file"""
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, 'r') as f:
                    data = json.load(f)
                    self.tasks = [Task.from_dict(task_data) for task_data in data]
            except (json.JSONDecodeError, KeyError): 
                """to manage if there was no tasks list"""
                print("Warning: Could not load tasks file. Starting Now")
                self.tasks = []
        else:
            self.tasks = []
    
    def save_tasks(self):
        """Save tasks to JSON file"""
        with open(DATA_FILE, 'w') as f:
            json.dump([task.to_dict() for task in self.tasks], f, indent=2)
    
    def add_task(self, title, due_date=None):
        """Add a new task"""
        task_id = self.get_next_id()
        task = Task(task_id, title, due_date)
        self.tasks.append(task)
        self.save_tasks()
        print(f"Task added successfully: {task}")
    
    def get_recent_tasks(self, count=3):
        """Get most recent tasks"""
        return sorted(self.tasks, key=lambda t: t.created_at, reverse=True)[:count]
    
    def get_task_history(self):
        """Get completed or failed tasks"""
        return [task for task in self.tasks if task.status in ["done", "failed"]]
    
    def get_pending_tasks(self):
        """Get pending tasks"""
        return [task for task in self.tasks if task.status == "pending"]
    
    def get_task_by_id(self, task_id):
        """Find task by ID"""
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None
    
    def get_task_by_name(self, title, exact_match=False):
        """Find task(s) by title/name"""
        if exact_match:
            return [task for task in self.tasks if task.title.lower() == title.lower()]
        else:
            return [task for task in self.tasks if title.lower() in task.title.lower()]
        
    def update_task_status(self, task_id, status):
        """Update task status"""
        task = self.get_task_by_id(task_id)
        if task:
            task.status = status
            self.save_tasks()
            return True
        return False
    
    def edit_task(self, task_id, new_title, new_due_date=None):
        """Edit task details"""
        task = self.get_task_by_id(task_id)
        if task:
            task.title = new_title
            if new_due_date is not None:
                task.due_date = new_due_date
            self.save_tasks()
            return True
        return False
    
    def remove_task(self, task_id):
        """Remove a task"""
        task = self.get_task_by_id(task_id)
        if task:
            self.tasks.remove(task)
            self.save_tasks()
            return True
        return False