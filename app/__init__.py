import os

from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail


import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

sentry_sdk.init(
    dsn="https://ecb51a077d15409da801b92c1e4884b5@o402962.ingest.sentry.io/5264949",
    integrations=[FlaskIntegration()],
)

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
        app.config["MAIL_SERVER"] = "smtp.sendgrid.net"
        app.config["MAIL_PORT"] = "587"
        app.config["MAIL_USERNAME"] = os.environ.get("SENDGRID_USERNAME")
        app.config["MAIL_PASSWORD"] = os.environ.get("SENDGRID_PASSWORD")
        mail.server = "smtp.sendgrid.net"
        mail.port = "587"
        mail.username = os.environ.get("SENDGRID_USERNAME")
        mail.password = os.environ.get("SENDGRID_PASSWORD")
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
