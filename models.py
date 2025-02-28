
class User:
    _id = 1
    _task_id = 1
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password
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


    def login(self, user):
        if user in self.users:
            self.current_user = user
            return True
        return False


    def add_task(self, title, due_date):
        if self.current_user:
            task = {
                "id": len(self.tasks) + 1,
                "user_id": self.current_user.user_id,
                "title": title,
                "due_data": due_date
            }
            self.tasks.append(task)
            return task
        return None


    def get_tasks(self):
        if self.current_user:
            return [task for task in self.tasks if task["user_id"] == self.current_user.user_id]
        return []


    def delete_task(self, task_id):
        if self.current_user:
            taske_to_delete = None
            for task in self.tasks:
                if task["id"] == task_id and task["user_id"] == self.current_user.user_id:
                    taske_to_delete = task
                    break
            if taske_to_delete:
                self.tasks.remove(taske_to_delete)
                return True
        return False
