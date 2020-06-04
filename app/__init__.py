import os

from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from rq import Queue
from flask_mail import Mail

from worker import conn

q = Queue(connection=conn)
db = SQLAlchemy()
migrate = Migrate()
mail = Mail()
jwt = JWTManager()


def create_app() -> Flask:
    app = Flask(__name__)
    if os.environ.get("TESTING"):
        app.config["TESTING"] = True
    CORS(app)

    @app.route("/")
    def index():
        return "Hello World!"

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
        os.curdir, "app.db"
    )
    if os.environ.get("DATABASE_URL"):
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_HEADER_TYPE"] = ""
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 3600
    app.config["SECRET_KEY"] = str(os.urandom(512))
    app.config["MAIL_SERVER"] = "localhost"
    app.config["MAIL_PORT"] = "25"
    if not os.environ.get("TESTING"):
        app.config["MAIL_SERVER"] = "smpt.sendgrid.net"
        app.config["MAIL_PORT"] = "587"
        app.config["MAIL_USERNAME"] = os.environ.get("SENDGRID_USERNAME")
        app.config["MAIL_PASSWORD"] = os.environ.get("SENDGRID_PASSWORD")
    if os.environ.get("SECRET_KEY"):
        app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    mail.init_app(app)

    # Register blueprints
    from app.auth import auth_blueprint
    from app.task import task_blueprint
    from app.house import house_blueprint

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(task_blueprint)
    app.register_blueprint(house_blueprint)

    return app
