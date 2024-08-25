import datetime

class Tasks:
    def __init__(self):
        self.tasks = {}

    def add_task(self, user_id, task_description, priority="medium", due_date=None):
        if user_id not in self.tasks:
            self.tasks[user_id] = []
        
        task = {
            "description": task_description,
            "priority": priority,
            "due_date": due_date,
            "created_at": datetime.datetime.now(),
            "completed": False
        }
        
        self.tasks[user_id].append(task)
        return f"Task added: {task_description}"

    def get_tasks(self, user_id):
        if user_id not in self.tasks or not self.tasks[user_id]:
            return "You have no tasks."
        
        task_list = []
        for i, task in enumerate(self.tasks[user_id]):
            status = "✓" if task["completed"] else "☐"
            due_date = f", due {task['due_date']}" if task['due_date'] else ""
            task_list.append(f"{i+1}. [{status}] {task['description']} (Priority: {task['priority']}{due_date})")
        
        return "Your tasks:\n" + "\n".join(task_list)

    def complete_task(self, user_id, task_index):
        if user_id not in self.tasks or task_index >= len(self.tasks[user_id]):
            return "Invalid task index."
        
        self.tasks[user_id][task_index]["completed"] = True
        return f"Task marked as completed: {self.tasks[user_id][task_index]['description']}"

    def remove_task(self, user_id, task_index):
        if user_id not in self.tasks or task_index >= len(self.tasks[user_id]):
            return "Invalid task index."
        
        removed_task = self.tasks[user_id].pop(task_index)
        return f"Removed task: {removed_task['description']}"

    def update_task_priority(self, user_id, task_index, new_priority):
        if user_id not in self.tasks or task_index >= len(self.tasks[user_id]):
            return "Invalid task index."
        
        self.tasks[user_id][task_index]["priority"] = new_priority
        return f"Updated priority for task: {self.tasks[user_id][task_index]['description']}"

    def set_due_date(self, user_id, task_index, due_date):
        if user_id not in self.tasks or task_index >= len(self.tasks[user_id]):
            return "Invalid task index."
        
        self.tasks[user_id][task_index]["due_date"] = due_date
        return f"Set due date for task: {self.tasks[user_id][task_index]['description']}"