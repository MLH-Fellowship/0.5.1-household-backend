from app import db
from werkzeug.security import generate_password_hash, check_password_hash

user_house = db.Table(
    "user_houses",
    db.Column("house_id", db.Integer, db.ForeignKey("house.id"), primary_key=True),
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
)


class House(db.Model):
    __tablename__ = "house"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True, nullable=False)
    description = db.Column(db.String(1024), nullable=False)

    tasks = db.relationship("Task", backref="house", lazy=True)
    users = db.relationship("User", secondary=user_house)


class Task(db.Model):
    __tablename__ = "task"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    house_id = db.Column(db.Integer, db.ForeignKey("house.id"), nullable=False)
    description = db.Column(db.String(1024), nullable=False)
    frequency = db.Column(db.Integer, nullable=False)

    user_tasks = db.relationship("UserTask", backref="user_task", lazy=True)


class UserTask(db.Model):
    __tablename__ = "user_task"
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey("task.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    deadline = db.Column(db.DateTime, nullable=False)
    done = db.Column(db.Boolean, nullable=False)


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email_verified = db.Column(db.Boolean, nullable=False)
    password_hash = db.Column(db.String(1024), nullable=False)

    houses = db.relationship("House", secondary=user_house)

    tasks = db.relationship("UserTask", backref="user")

    def set_password(self, password) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password) -> bool:
        return check_password_hash(self.password_hash, password)


class WorkerTask(db.Model):
    __tablename__ = "worker_task"
    id = db.Column(db.Integer, primary_key=True)
    complete_at = db.Column(db.DateTime)
    task_type = db.Column(db.Integer)
    context = db.Column(db.String(1024), nullable=False)
