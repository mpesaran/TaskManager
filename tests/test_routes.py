import sys
import os
import pytest
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app


@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })
    yield app


@pytest.fixture
def client(app):
    "A test client for the app"
    with app.test_client() as client:
        yield client

@pytest.fixture
def valid_user():
    """Fixture to provide a valid user dictionary."""
    return {
        "name": "Alice",
        "email": "alice@exxample.com",
        "password": "pass123"
    }

class TestEndPoints:
    def test_register_user(self, client, valid_user):
        """Test registering a new user"""
        response = client.post('/api/register', json=valid_user)
        assert response.status_code == 201
        assert "user_id" in response.json

    def test_login_user(self, client, valid_user):
        """Test login a registerd user"""
        response = client.post('/api/login', json={"email":"alice@exxample.com", "password":"pass123"})
        assert response.status_code == 200
        

    def test_add_task(self, client, valid_user):
        """Test adding a task for the logged-in user"""
        task = {
            "title": "Finish project",
            "due_date": "25-01-25"
        }
        response = client.post('/api/add_task', json=task)
        assert response.status_code == 201
        assert "task_id" in response.json

    def test_get_tasks(self, client, valid_user):
        """Test retrieving tasks for the logged-in user"""
        register_response = client.post('/api/register', json=valid_user)
        assert register_response.status_code == 201
        user_id = register_response.json["user_id"]
    
        # Then, log in the user
        login_response = client.post('/api/login', json={"email": valid_user["email"], "password": valid_user["password"]})
        assert login_response.status_code == 200
        response = client.get('api/user/tasks')
        assert response.status_code == 200
        assert "tasks" in response.json
        assert isinstance(response.json["tasks"], list)
        assert len(response.json["tasks"]) > 0

    def test_delete_task(self, client, valid_user):
        """Test deleting a task for the logged-in user"""
        task_id = 1
        response = client.delete(f'/api/delete/tasks/{task_id}')
        assert response.status_code == 200
        assert response.json["message"] == "Task deleted successsfully"

    def test_delete_task_not_owned_by_user(self, client, valid_user):
        """Test trying to delete a task not owned by the logged-in user"""
        task_id = 999
        response = client.delete(f'/api/delete/tasks/{task_id}')
        assert response.status_code == 404
        assert response.json["error"] == "Task not found"