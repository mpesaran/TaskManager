from flask import Flask


def create_app():

    app = Flask(__name__)
    app.secret_key = 'top_secret'
    
    """
    Without this import, routes.py file is being imported before app is properly initialized, causing
    routes not being registered. The reponse for unregistered route is 404 Not Found
    """
    #Import routes AFTER creating the app instance
    # from app.routes import register_routes
    # register_routes(app)
    from app.routes import task_manager_bp
    app.register_blueprint(task_manager_bp, url_prefix='/api/')
    return app

