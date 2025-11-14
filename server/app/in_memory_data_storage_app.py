from flask import Flask, jsonify, request
from datetime import datetime

app = Flask(__name__)

# -----------------------------
# Global data storage
# -----------------------------
tasks = []
categories = []
task_id_counter = 1


# -----------------------------
# Basic routes
# -----------------------------
@app.route('/')
def home():
    return jsonify({'message': 'Welcome to Task Manager API', 'status': 'running'})


@app.route('/api/info')
def info():
    return jsonify({
        'app_name': 'Task Manager',
        'version': '2.0',
        'features': ['categories', 'due dates', 'stats', 'priority']
    })


# -----------------------------
# CATEGORY ROUTES
# -----------------------------
@app.route('/api/categories', methods=['POST'])
def create_category():
    data = request.get_json()
    name = data.get('name')

    if not name:
        return jsonify({'error': 'Category name is required'}), 400
    if name in [c['name'] for c in categories]:
        return jsonify({'error': 'Category already exists'}), 400

    categories.append({'name': name})
    return jsonify({'message': 'Category created', 'category': name}), 201


@app.route('/api/categories', methods=['GET'])
def get_categories():
    return jsonify({'categories': categories, 'count': len(categories)}), 200


# -----------------------------
# TASK ROUTES
# -----------------------------
@app.route('/api/tasks', methods=['POST'])
def create_task():
    global task_id_counter
    data = request.get_json()

    # Get fields with defaults
    title = data.get('title', 'Untitled Task')
    description = data.get('description', '')
    category = data.get('category', 'General')
    due_date = data.get('due_date')
    priority = data.get('priority', 'medium')

    # Validate due_date format (must be YYYY-MM-DD)
    if due_date:
        datetime.strptime(due_date, '%Y-%m-%d')

    new_task = {
        'id': task_id_counter,
        'title': title,
        'description': description,
        'category': category,
        'priority': priority,
        'completed': False,
        'due_date': due_date
    }

    tasks.append(new_task)
    task_id_counter += 1

    return jsonify({'message': 'Task created', 'task': new_task}), 201


@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks, 'count': len(tasks)}), 200


@app.route('/api/tasks/category/<string:category>', methods=['GET'])
def get_tasks_by_category(category):
    filtered = [t for t in tasks if t.get('category') == category]
    return jsonify({'category': category, 'tasks': filtered, 'count': len(filtered)}), 200


@app.route('/api/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    for task in tasks:
        if task['id'] == task_id:
            return jsonify(task), 200
    return jsonify({'error': 'Task not found'}), 404


@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.get_json()
    for task in tasks:
        if task['id'] == task_id:
            task['title'] = data.get('title', task['title'])
            task['description'] = data.get('description', task['description'])
            task['category'] = data.get('category', task['category'])
            task['priority'] = data.get('priority', task['priority'])
            task['completed'] = data.get('completed', task['completed'])
            task['due_date'] = data.get('due_date', task['due_date'])
            return jsonify({'message': 'Task updated', 'task': task}), 200
    return jsonify({'error': 'Task not found'}), 404


@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    global tasks
    for task in tasks:
        if task['id'] == task_id:
            tasks = [t for t in tasks if t['id'] != task_id]
            return jsonify({'message': f'Task {task_id} deleted successfully'}), 200
    return jsonify({'error': 'Task not found'}), 404


# -----------------------------
# DUE DATE AND STATS
# -----------------------------
@app.route('/api/tasks/overdue', methods=['GET'])
def get_overdue_tasks():
    today = datetime.now().date()
    overdue = []

    for task in tasks:
        if task['due_date'] and not task['completed']:
            due = datetime.strptime(task['due_date'], '%Y-%m-%d').date()
            if due < today:
                overdue.append(task)

    return jsonify({'overdue_tasks': overdue, 'count': len(overdue)}), 200


@app.route('/api/tasks/stats', methods=['GET'])
def get_stats():
    total = len(tasks)
    completed = len([t for t in tasks if t['completed']])
    pending = total - completed
    overdue = 0
    today = datetime.now().date()

    for task in tasks:
        if task['due_date'] and not task['completed']:
            due = datetime.strptime(task['due_date'], '%Y-%m-%d').date()
            if due < today:
                overdue += 1

    return jsonify({
        'total_tasks': total,
        'completed': completed,
        'pending': pending,
        'overdue': overdue
    }), 200


# -----------------------------
# Run the Flask app
# -----------------------------
if __name__ == '__main__':
    app.run(debug=True, port=5100)
