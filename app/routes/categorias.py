from flask import Blueprint, render_template

bp = Blueprint("categorias", __name__, url_prefix="/categorias")

@bp.route("/")
def index():
    return render_template("categorias.html", title="Gastos por categoría")
