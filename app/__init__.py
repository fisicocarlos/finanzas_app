import logging

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config.config import APP_NAME, SQLALCHEMY_DATABASE_URI
from app.models import Base


db = SQLAlchemy(model_class=Base)


def create_app():
    app = Flask(__name__)
    app.logger = logging.getLogger(APP_NAME)

    app.logger.info("Starting app")

    app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
    db.init_app(app)

    from app.routes import categorias, dashboard, viajes

    app.register_blueprint(dashboard.bp)
    app.register_blueprint(viajes.bp)
    app.register_blueprint(categorias.bp)

    return app
