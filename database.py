from flask_sqlalchemy import SQLAlchemy
from flask import Flask

db = SQLAlchemy()


def create_app():
    app = Flask(__name__, static_url_path="/static")
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///crm.db"
    # Other configurations

    # Initialize extensions
    db.init_app(app)

    return app
