from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
import os

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()


def create_app() -> Flask:
    app = Flask(__name__)

    @app.route("/")
    def index():
        return "Hello World!"

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + \
        os.path.join(os.curdir, "app.db")
    if os.environ.get("DATABASE_URL"):
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = str(os.urandom(512))
    if os.environ.get("SECRET_KEY"):
        app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    from app.auth import auth_blueprint
    app.register_blueprint(auth_blueprint)
    return app
