from werkzeug.security import generate_password_hash, check_password_hash

class User:
    _id = 1
    _task_id = 1
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password_hash = generate_password_hash(password)
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


    def register_user(self, name, email, password):
        user = User(name, email, password)
        self.users.append(user)
        return user


    def login(self, email, password):
        user = next((u for u in self.users if u.email == email), None) # find user by email
        if user and check_password_hash(user.password_hash, password):
            self.current_user = user
            return user
        return None


    def add_task(self, title, due_date):
        if self.current_user:
            task = {
                "task_id": len(self.tasks) + 1,
                "user_id": self.current_user.user_id,
                "title": title,
                "due_data": due_date
            }
            self.tasks.append(task)
            return task
        return None


    def get_tasks(self, user_id):
        if self.current_user.user_id == user_id:
            return [task for task in self.tasks if task["user_id"] == user_id]
        return []


    def delete_task(self, task_id):
        if self.current_user:
            taske_to_delete = None
            for task in self.tasks:
                if task["task_id"] == int(task_id) and task["user_id"] == self.current_user.user_id:
                    taske_to_delete = task
                    break
            if taske_to_delete:
                self.tasks.remove(taske_to_delete)
                return True
        return False
