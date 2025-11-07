from flask import Blueprint, render_template

from app.data.drive_reader import load_data
from app.data.processor import balance_per_month

bp = Blueprint("dashboard", __name__, url_prefix="/")


@bp.route("/")
def index():
    df = load_data()
    balance_per_month_table = balance_per_month(df).to_html(index_names=False)

    return render_template(
        "dashboard.html",
        title="Resumen general",
        balance_per_month_table=balance_per_month_table,
    )
