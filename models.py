
class User:
    _id = 1
    _task_id = 1
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.user_id = User._id
        self.tasks = []
        User._id += 1

    def add_task(self, title, due_date):
        task = {
            "id": User._task_id,
            "title": title,
            "due_date": due_date
        }
        self.tasks.append(task)
        User._task_id += 1
        return task
    
    def get_task(self):
        return self.tasks


class TaskManager:
    def __init__(self):
        self.users = []
        self.tasks = []
        self.current_user = None
    
    def register_user(self, name, email):
        user = User(name, email)
        self.users.append(user)
        return user
    
    def login(self, user):
        if user in self.users:
            self.current_user = user
            return True
        return False