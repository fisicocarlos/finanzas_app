from flask import Blueprint, render_template

from app.data.drive_reader import load_data
from app.data.plots import gastos_mensuales

bp = Blueprint("dashboard", __name__, url_prefix="/")


@bp.route("/")
def index():
    df = load_data()
    gastos_mensuales_plot = gastos_mensuales(df)
    return render_template(
        "dashboard.html",
        title="Resumen general",
        gastos_mensuales_plot=gastos_mensuales_plot,
    )
