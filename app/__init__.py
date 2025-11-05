from flask import Flask

def create_app():
    app = Flask(__name__)

    # Registrar rutas
    from app.routes import dashboard, viajes, categorias
    app.register_blueprint(dashboard.bp)
    app.register_blueprint(viajes.bp)
    app.register_blueprint(categorias.bp)

    return app
