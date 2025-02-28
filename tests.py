import pytest
from models import User, TaskManager

@pytest.fixture(autouse=True)
def reset_ids():
    User._id = 1
    User._task_id = 1

@pytest.fixture
def user():
    return User("Alice", "alice@example.com", "pass123")

@pytest.fixture
def task_manager():
    return TaskManager()

@pytest.fixture
def logged_in_user(task_manager):
    user = task_manager.register_user("Alice", "alice@example.com", "password123")
    task_manager.login(user)  
    return user

class TestUserClass:
    def test_create_user(self,user):
        assert user.user_id == 1
        assert user.name == "Alice"
        assert user.email == "alice@example.com"

        user2 = User("Ale", "ale@example.com", "pass123")
        assert user2.user_id == 2
        assert user2.name == "Ale"
        assert user2.email == "ale@example.com"

    def test_add_task(self, user):
        task1 = user.add_task("Complete project", "2025-03-10")
        assert task1 == {
                "id": 1,
                "title": "Complete project",
                "due_date": "2025-03-10"
            }
        assert len(user.tasks) == 1

    def test_get_task(self, user):
        user.add_task("Complete project", "2025-03-10")
        user.add_task("Submit report", "2025-03-15")
        
        assert user.get_task() == [
            {"id": 1, "title": "Complete project", "due_date": "2025-03-10"},
            {"id": 2, "title": "Submit report", "due_date": "2025-03-15"}
        ]
        assert isinstance(user.get_task(), list)
        assert len(user.get_task()) == 2

class TestTaskManagerClass:
    def test_register_user(self, task_manager):
        user =task_manager.register_user("Alice", "alice@example.com", "pass123")
        assert user.user_id == 1
        assert user.name == "Alice"
        assert user.email == "alice@example.com"


    def test_login_user(self, task_manager, logged_in_user):
        assert task_manager.current_user == logged_in_user

    def test_add_task(self, task_manager, logged_in_user):
        task = task_manager.add_task("Complete project", "2025-03-10")

        assert task ==  {
                "id": 1,
                "user_id": 1,
                "title": "Complete project",
                "due_data": "2025-03-10"
            }
        assert len(task_manager.tasks) == 1

    def test_retrieve_user_tasks(self, task_manager, logged_in_user):

        task_manager.add_task("Complete project", "2025-03-10")
        task_manager.add_task("Submit report", "2025-03-15")
        tasks = task_manager.get_tasks()
        assert tasks[0]["title"] == "Complete project"
        assert tasks[1]["title"] == "Submit report"
        assert len(tasks) == 2

    def test_task_delete(self, task_manager, logged_in_user):

        task_manager.add_task("Complete project", "2025-03-10")
        task_manager.add_task("Submit report", "2025-03-15")
        assert task_manager.delete_task(1) is True
        assert len(task_manager.tasks) == 1
        assert task_manager.tasks[0]["title"] == "Submit report"

        assert task_manager.delete_task(2) is True
        assert len(task_manager.tasks) == 0
        assert task_manager.get_tasks() == []

    def test_delete_task_not_owned_by_user(self, task_manager):
        user1 = task_manager.register_user("Alice", "alice@example.com", "password123")
        user2 = task_manager.register_user("Bob", "bob@example.com", "password123")
        task_manager.login(user1)
        task_manager.add_task("Complete project", "2025-03-10")
        task_manager.login(user2)
        task_manager.add_task("Submit report", "2025-03-15")

        assert task_manager.delete_task(1) is False
        assert len(task_manager.tasks) == 2
        assert len([task for task in task_manager.tasks if task["user_id"] ==  user1.user_id]) == 1
        assert len([task for task in task_manager.tasks if task["user_id"] ==  user2.user_id]) == 1
