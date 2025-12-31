from flask import Blueprint, render_template

from app.components.tables import categories_table

bp = Blueprint("categorias", __name__, url_prefix="/categorias")


@bp.route("/")
def index():
    return render_template(
        "categories.html",
        title="Gastos por categoría",
        categories_table_html=categories_table(),
    )
