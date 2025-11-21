from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# --------------------- DATABASE CONFIG ---------------------
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:passw0rd@localhost:3308/app_db?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# PART 1: USER MODEL


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    tasks = db.relationship("Task", backref="user", lazy=True)


# Task model with user_id FK (Part 3 requirement)
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)


# Create tables
with app.app_context():
    db.create_all()


# PART 2: USER CRUD ENDPOINTS


# Create User
@app.route("/api/users", methods=["POST"])
def create_user():
    data = request.json
    user = User(username=data["username"], email=data["email"])
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User created", "user_id": user.id}), 201


# List All Users
@app.route("/api/users", methods=["GET"])
def get_users():
    users = User.query.all()
    return jsonify([
        {"id": u.id, "username": u.username, "email": u.email, "created_at": u.created_at}
        for u in users
    ])


# Get Single User
@app.route("/api/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "created_at": user.created_at
    })


# Update User
@app.route("/api/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.json

    user.username = data.get("username", user.username)
    user.email = data.get("email", user.email)

    db.session.commit()
    return jsonify({"message": "User updated"})


# Delete User
@app.route("/api/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted"})



# PART 3: LINK TASKS TO USERS


# Create Task assigned to a user
@app.route("/api/tasks", methods=["POST"])
def create_task():
    data = request.json
    task = Task(
        title=data["title"],
        description=data.get("description"),
        user_id=data["user_id"]  # Accept user_id from request
    )
    db.session.add(task)
    db.session.commit()
    return jsonify({"message": "Task created", "task_id": task.id})


# Get All Tasks of a User
@app.route("/api/users/<int:user_id>/tasks", methods=["GET"])
def get_user_tasks(user_id):
    tasks = Task.query.filter_by(user_id=user_id).all()
    return jsonify([
        {"id": t.id, "title": t.title, "description": t.description}
        for t in tasks
    ])


if __name__ == "__main__":
    app.run(debug=True, port=5200)

