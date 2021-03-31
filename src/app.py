from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
# Database connection                        ↓ Using pymysql
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root@localhost/flask_mysql"
# Prevents database warnings when app is running
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# database instance with SQLAlchemy
db = SQLAlchemy(app)

# Marshmallow helps with creating a Schema
marshmallow = Marshmallow(app)

# Definition of the Task model
class Task(db.Model):  # class x(inherits):
    id = db.Column(db.Integer, primary_key=True)
    # 70 is the mas length allowed
    title = db.Column(db.String(70), unique=True)
    description = db.Column(db.String(100))  # 100 is the mas length allowed

    def __init__(self, title, description):
        self.title = title
        self.description = description


# Creates the Database tables
db.create_all()

# Task Schema
class TaskSchema(marshmallow.Schema):  # class x(inherits):
    class Meta:
        # Fields when intercating with this Schema
        fields = ("id", "title", "description")


# when creating a single task
task_schema = TaskSchema()
# when creating a multiple tasks
tasks_schema = TaskSchema(many=True)

# Routes
@app.route("/tasks", methods=["POST"])
def create_task():

    # Elements from the request body
    title = request.json["title"]
    description = request.json["description"]

    # New task schema
    new_task = Task(title, description)

    # Saving task in db
    db.session.add(new_task)
    db.session.commit()  # end of db operation

    return task_schema.jsonify(new_task)


@app.route("/tasks", methods=["GET"])
def get_tasks():
    # Model to get all the tasks
    all_tasks = Task.query.all()
    # queries the tasks from the database
    results = tasks_schema.dump(all_tasks)

    return jsonify(results)


@app.route("/tasks/<id>", methods=["GET"])
def get_task(id):
    task = Task.query.get(id)
    return task_schema.jsonify(task)


@app.route("/tasks/<id>", methods=["PUT"])
def update_task(id):
    task = Task.query.get(id)

    title = request.json["title"]
    description = request.json["description"]

    task.title = title
    task.description = description

    db.session.commit()

    return task_schema.jsonify(task)


@app.route("/tasks/<id>", methods=["DELETE"])
def delete_task(id):
    task = Task.query.get(id)
    db.session.delete(task)
    db.session.commit()

    return task_schema.jsonify(task)


@app.route("/", methods=["GET"])
def index():
    return jsonify({"message": "Welcome to my API"})


if __name__ == "__main__":
    app.run(debug=True)
