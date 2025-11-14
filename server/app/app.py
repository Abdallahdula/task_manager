from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify ({
    'message': 'Welcome to Task Manager API',
    'status': 'running'
    })

@app.route('/hello')
def hello():
    return jsonify ({
    'message': 'Hello, World!'})

@app.route('/api/info')
def info():
    return jsonify ({
    'app_name': 'Task Manager',
    'version': '1.0',
    'author': 'omsekhar'
    })

@app.route('/api/status')
def status():
    return jsonify ({
    'database': 'connected',
    'server': 'running',
    'uptime': '24 hours'
    })

@app.route('/api/greet')
def greet():
    name = request.args.get('name','Guest')

    return jsonify ({
    'message': f'Hello, {name}!',
    'greeting': 'Welcome to Task Manager'
    })
@app.route('/api/add')
def add():
    a = request.args.get('a',5)
    b = request.args.get('b', 3)

    # Convert them to integers
    a = int(a)
    b = int(b)

    # Add them together
    c = a + b

    # Return the result as JSON
    return jsonify({
        'result': c,
        'operation': 'addition'
    })
tasks = []
task_id_counter = 1
@app.route('/api/tasks', methods=['POST'])
def create_tasks():
    global task_id_counter
    data = request.get_json()
    new_task = {
     'id' : task_id_counter,
     'title' : data.get('title'),
     'description' : data.get('description'),
     'completed' : False
    }
    tasks.append(new_task)
    task_id_counter += 1

    return jsonify(new_task), 201

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    return jsonify({
        'tasks': tasks,
        'count': len(tasks)
    }) , 200
@app.route('/api/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = next((t for t in tasks if t['id'] == task_id), None)
    if task is None:
        return jsonify({'error' : 'Task not found'}), 404
    return jsonify(task), 200

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.get_json()
    for task in tasks:
        if task['id'] == task_id:
            task['title'] = data.get('title', task['title'])
            task['description'] = data.get('description', task['description'])
            task['completed'] = data.get('completed', task['completed'])
            return jsonify({
                'message': 'Task updated successfully',
                'task': task
            }), 200
    return jsonify({'error': 'Task not found'}), 404


@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    for task in tasks:
        if task['id'] == task_id:
            tasks.remove(task)
            return jsonify({
                'message': 'Task deleted successfully'
            }), 200
    return jsonify({'error': 'Task not found'}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)