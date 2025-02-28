import pytest
from models import User, TaskManager

@pytest.fixture(autouse=True)
def reset_ids():
    User._id = 1
    User._task_id = 1

@pytest.fixture
def user():
    return User("Alice", "alice@example.com")

@pytest.fixture
def task_manager():
    return TaskManager()

class TestUserClass:
    def test_create_user(self,user):
        assert user.user_id == 1
        assert user.name == "Alice"
        assert user.email == "alice@example.com"

        user2 = User("Ale", "ale@example.com")
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
        user =task_manager.register_user("Alice", "alice@example.com")
        assert user.user_id == 1
        assert user.name == "Alice"
        assert user.email == "alice@example.com"


    def test_login_user(self, task_manager):
        user1 = task_manager.register_user("Alice", "alice@example.com")
        task_manager.login(user1)
        assert task_manager.current_user == user1

    def test_add_task(self, task_manager):
        user1 = task_manager.register_user("Alice", "alice@example.com")
        task_manager.login(user1)

        task = task_manager.add_task("Complete project", "2025-03-10")

        assert task ==  {
                "id": 1,
                "title": "Complete project",
                "due_date": "2025-03-10"
            }      