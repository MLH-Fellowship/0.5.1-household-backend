from app import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(64), index=True, unique=True)
    email_verified = db.Column(db.Boolean)
    password_hash = db.Column(db.String(1024))

    def set_password(self, password) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password) -> bool:
        return check_password_hash(self.password_hash, password)

class House(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    description = db.Column(db.String(1024))

    def update_invite_link(self, link) -> None:
        self.invite_link = link

class UserHouse(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    house_id = db.Column(db.Integer, primary_key=True)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    house_id = db.Column(db.Integer)
    description= db.Column(db.String(1024))
    frequency = db.Column(db.Integer)

class UserTask(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, primary_key=True)
    deadline = db.Column(db.DateTime)
    # done
