from flask import Flask, jsonify
from database import init_db
from routes.auth import auth_bp
from routes.tasks import tasks_bp


def create_app() -> Flask:
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'change-this-in-production'
    app.config['DATABASE'] = 'instance/task_manager.db'

    init_db(app)

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(tasks_bp, url_prefix='/tasks')

    @app.get('/')
    def home():
        return jsonify({
            'message': 'Task Manager API is running',
            'endpoints': {
                'register': 'POST /auth/register',
                'login': 'POST /auth/login',
                'list_tasks': 'GET /tasks',
                'create_task': 'POST /tasks',
                'update_task': 'PUT /tasks/<task_id>',
                'delete_task': 'DELETE /tasks/<task_id>'
            }
        })

    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
