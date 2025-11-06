import logging

from flask import Flask

from app.config.config import APP_NAME


def create_app():
    app = Flask(__name__)
    app.logger = logging.getLogger(APP_NAME)
    app.logger.info("Starting app")

    # Registrar rutas
    from app.routes import categorias, dashboard, viajes

    app.register_blueprint(dashboard.bp)
    app.register_blueprint(viajes.bp)
    app.register_blueprint(categorias.bp)

    return app
