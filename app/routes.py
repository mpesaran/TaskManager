from flask import request, jsonify, session, Blueprint
from app.models import TaskManager

# Create a Blueprint
task_manager_bp = Blueprint('task_manager', __name__)

# Initialize TaskManager instance
task_manager = TaskManager()


@task_manager_bp.route("/register", methods=['POST'])
def register_user():
    """Register user with the """
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    if not name or not email or not password:
        return jsonify({"error": "missing required fields"}), 400
    user = task_manager.register_user(name, email, password)
    return jsonify({"message": f"User {name} registered.", "user_id": user.user_id}), 201


@task_manager_bp.route("/login", methods=['POST'])
def login_user():
    "Login user with credentials"
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    user = task_manager.login(email, password)
    if not user:
        return jsonify({"error": "Invalid credentials"}), 401
    session['user_id'] = user.user_id

    return jsonify({'message': f"{user.name} logged in successfully"}), 200


@task_manager_bp.route('/user/tasks', methods=['GET'])
def get_user_tasks():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': "User not logged in"})
    tasks = task_manager.get_tasks(user_id)
    if tasks:
        return jsonify({"user": user_id, "tasks": tasks}), 200
    return jsonify({'error': 'No tasks found for the user'}), 404


@task_manager_bp.route('/add_task', methods=['POST'])
def add_task_to_list():
    data = request.get_json()
    title = data.get("title")
    due_date = data.get("due_date")
    if not title or not due_date:
        return jsonify({'error': "missing required fields"}), 400
    task = task_manager.add_task(title, due_date)
    return jsonify({'message': "Task added successfully", "task_id": task["task_id"]}), 201


@task_manager_bp.route('/delete/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    success = task_manager.delete_task(task_id)
    if success:
        return jsonify({'message': "Task deleted successsfully"}), 200
    return jsonify({"error": "Task not found"}), 404