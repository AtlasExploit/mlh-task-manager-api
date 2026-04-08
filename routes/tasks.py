from functools import wraps
import jwt
from flask import Blueprint, current_app, jsonify, request
from database import get_db

tasks_bp = Blueprint('tasks', __name__)


def token_required(view_func):
    @wraps(view_func)
    def wrapped(*args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        parts = auth_header.split()

        if len(parts) != 2 or parts[0].lower() != 'bearer':
            return jsonify({'error': 'missing or invalid bearer token'}), 401

        token = parts[1]
        try:
            payload = jwt.decode(
                token,
                current_app.config['SECRET_KEY'],
                algorithms=['HS256']
            )
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'invalid token'}), 401

        request.user_id = payload['user_id']
        return view_func(*args, **kwargs)

    return wrapped


@tasks_bp.get('')
@token_required
def list_tasks():
    db = get_db()
    tasks = db.execute(
        'SELECT id, title, description, completed FROM tasks WHERE user_id = ? ORDER BY id DESC',
        (request.user_id,)
    ).fetchall()

    return jsonify([
        {
            'id': task['id'],
            'title': task['title'],
            'description': task['description'],
            'completed': bool(task['completed'])
        }
        for task in tasks
    ])


@tasks_bp.post('')
@token_required
def create_task():
    data = request.get_json(silent=True) or {}
    title = data.get('title', '').strip()
    description = data.get('description', '').strip()

    if not title:
        return jsonify({'error': 'title is required'}), 400

    db = get_db()
    cursor = db.execute(
        'INSERT INTO tasks (title, description, user_id) VALUES (?, ?, ?)',
        (title, description, request.user_id)
    )
    db.commit()

    return jsonify({
        'message': 'task created successfully',
        'task_id': cursor.lastrowid
    }), 201


@tasks_bp.put('/<int:task_id>')
@token_required
def update_task(task_id: int):
    data = request.get_json(silent=True) or {}
    title = data.get('title')
    description = data.get('description')
    completed = data.get('completed')

    db = get_db()
    task = db.execute(
        'SELECT id FROM tasks WHERE id = ? AND user_id = ?',
        (task_id, request.user_id)
    ).fetchone()

    if not task:
        return jsonify({'error': 'task not found'}), 404

    current_task = db.execute(
        'SELECT title, description, completed FROM tasks WHERE id = ? AND user_id = ?',
        (task_id, request.user_id)
    ).fetchone()

    updated_title = title.strip() if isinstance(title, str) and title.strip() else current_task['title']
    updated_description = description.strip() if isinstance(description, str) else current_task['description']
    updated_completed = int(bool(completed)) if completed is not None else current_task['completed']

    db.execute(
        'UPDATE tasks SET title = ?, description = ?, completed = ? WHERE id = ? AND user_id = ?',
        (updated_title, updated_description, updated_completed, task_id, request.user_id)
    )
    db.commit()

    return jsonify({'message': 'task updated successfully'})


@tasks_bp.delete('/<int:task_id>')
@token_required
def delete_task(task_id: int):
    db = get_db()
    task = db.execute(
        'SELECT id FROM tasks WHERE id = ? AND user_id = ?',
        (task_id, request.user_id)
    ).fetchone()

    if not task:
        return jsonify({'error': 'task not found'}), 404

    db.execute(
        'DELETE FROM tasks WHERE id = ? AND user_id = ?',
        (task_id, request.user_id)
    )
    db.commit()

    return jsonify({'message': 'task deleted successfully'})
