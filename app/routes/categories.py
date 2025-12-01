from flask import Blueprint, render_template

from app.data.processor import categories_table

bp = Blueprint("categorias", __name__, url_prefix="/categorias")


@bp.route("/")
def index():
    categories_table_html = categories_table()
    print(categories_table_html)
    return render_template(
        "categories.html",
        title="Gastos por categoría",
        categories_table_html=categories_table_html,
    )
