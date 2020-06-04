from app import db
from werkzeug.security import generate_password_hash, check_password_hash

user_house = db.Table(
    "user_houses",
    db.Column("house_id", db.Integer, db.ForeignKey("house.id"), primary_key=True),
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
)


class House(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    description = db.Column(db.String(1024))


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    house_id = db.Column(db.Integer, db.ForeignKey("house.id"))
    description = db.Column(db.String(1024))
    frequency = db.Column(db.Integer)

    user_tasks = db.relationship("UserTask", backref="task", lazy=True)


class UserTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey("task.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    deadline = db.Column(db.DateTime)
    done = db.Column(db.Boolean)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(64), index=True, unique=True)
    email_verified = db.Column(db.Boolean)
    password_hash = db.Column(db.String(1024))

    houses = db.relationship("House", secondary=user_house)

    tasks = db.relationship("UserTask", secondary="user_task")

    def set_password(self, password) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password) -> bool:
        return check_password_hash(self.password_hash, password)
