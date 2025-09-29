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

class TaskManagerApp:
    def __init__(self):
        self.task_manager = TaskManager()
    
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def get_input(self, prompt):
        return input(f"{prompt}: ").strip()
    
    def display_tasks(self, tasks, title="Tasks"):
        print(f"\n--- {title} ---")
        if not tasks:
            print("No tasks found.")
            return
        for task in tasks:
            print(task)
    
    def startup_menu(self):
        while True:
            self.clear_screen()
            print("*** TASK MANAGER ***")
            print("\n1- Tasks")
            print("2- Task history")
            print("3- Exit")
            
            choice = self.get_input("Select an option")
            
            if choice == "1":
                self.tasks_menu()
            elif choice == "2":
                self.task_history_menu()
            elif choice == "3":
                break
    
    def tasks_menu(self):
        while True:
            self.clear_screen()
            print("*** TASKS MENU ***")
            recent_tasks = self.task_manager.get_recent_tasks(3)
            self.display_tasks(recent_tasks, "Recent Tasks")
            
            print("\n1- Add New Task")
            print("2- Task List")
            print("3- Task Manager")
            print("4- Back")
            
            choice = self.get_input("Select an option")
            
            if choice == "1":
                self.add_task_menu()
            elif choice == "2":
                self.task_list_menu()
            elif choice == "3":
                self.task_manager_menu()
            elif choice == "4":
                break
    
    def add_task_menu(self):
        self.clear_screen()
        print("*** ADD NEW TASK ***")
        title = self.get_input("Task title")
        if not title:
            return
        due_date = self.get_input("Due date (YYYY-MM-DD) or skip")
        due_date = due_date if due_date else None
        self.task_manager.add_task(title, due_date)
    
    def task_list_menu(self):
        current_page = 0
        while True:
            self.clear_screen()
            print("*** TASK LIST ***")
            pending_tasks = self.task_manager.get_pending_tasks()
            start_idx = current_page * 5
            end_idx = start_idx + 5
            page_tasks = pending_tasks[start_idx:end_idx]
            self.display_tasks(page_tasks, f"Page {current_page + 1}")
            print(f"\nShowing {start_idx + 1}-{min(end_idx, len(pending_tasks))} of {len(pending_tasks)}")
            
            print("\n1- Next 5")
            print("2- Previous 5")
            print("3- Show All")
            print("4- Back")
            
            choice = self.get_input("Select an option")
            
            if choice == "1" and end_idx < len(pending_tasks):
                current_page += 1
            elif choice == "2" and current_page > 0:
                current_page -= 1
            elif choice == "3":
                self.clear_screen()
                self.display_tasks(pending_tasks, "All Tasks")
                input()
            elif choice == "4":
                break
    
    def task_manager_menu(self):
        while True:
            self.clear_screen()
            print("*** TASK MANAGER ***")
            pending_tasks = self.task_manager.get_pending_tasks()
            self.display_tasks(pending_tasks, "Pending Tasks")
            
            print("\n1- Tick task")
            print("2- Cross task")
            print("3- Edit task")
            print("4- Remove task")
            print("5- Back")
            
            choice = self.get_input("Select an option")
            
            if choice == "1":
                task_id = int(self.get_input("Task ID"))
                self.task_manager.update_task_status(task_id, "done")
            elif choice == "2":
                task_id = int(self.get_input("Task ID"))
                self.task_manager.update_task_status(task_id, "failed")
            elif choice == "3":
                self.edit_task_menu()
            elif choice == "4":
                task_id = int(self.get_input("Task ID"))
                self.task_manager.remove_task(task_id)
            elif choice == "5":
                break
    
    def edit_task_menu(self):
        task_id = int(self.get_input("Task ID"))
        task = self.task_manager.get_task_by_id(task_id)
        if not task:
            return
        print(f"Current: {task}")
        new_title = self.get_input("New title") or task.title
        new_due_date = self.get_input("New due date") or task.due_date
        self.task_manager.edit_task(task_id, new_title, new_due_date)
    
    def task_history_menu(self):
        self.clear_screen()
        print("*** TASK HISTORY ***")
        completed_tasks = self.task_manager.get_task_history()
        self.display_tasks(completed_tasks, "History")
        input()
    
    def run(self):
        self.startup_menu()


def main():
    """Main function"""
    app = TaskManagerApp()
    app.run()


if __name__ == "__main__":
    main()