from app import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(64), index=True, unique=True)
    email_verified = db.Column(db.Boolean)
    password_hash = db.Column(db.String(1024))

    houses = db.relationship(
        "House",
        secondary=user_house,
        lazy="subquery",
        backref=db.backref("users", lazy=True),
    )

    def set_password(self, password) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password) -> bool:
        return check_password_hash(self.password_hash, password)


class House(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    description = db.Column(db.String(1024))
    users = db.relationship(
        "User",
        secondary=user_house,
        lazy="subquery",
        backref=db.backref("houses", lazy=True),
    )


user_house = db.Table(
    db.Column("house_id", db.Integer, db.ForeignKey("house.id"), primary_key=True),
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    house_id = db.Column(db.Integer, db.ForeignKey("house.id"))
    description = db.Column(db.String(1024))
    frequency = db.Column(db.Integer)


class UserTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey("task.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    deadline = db.Column(db.DateTime)
    done = db.Column(db.Boolean)
