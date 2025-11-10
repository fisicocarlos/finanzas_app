from flask import Blueprint, render_template

from app.data.drive_reader import load_data
from app.data.processor import balance_per_month, last_movements
from app.data.plots import bar_plot_per_categories, pie_plot_per_categories

bp = Blueprint("dashboard", __name__, url_prefix="/")


@bp.route("/")
def index():
    df = load_data()
    balance_per_month_table = balance_per_month(df).to_html(index_names=False)
    last_movements_table = last_movements(df, 5).to_html(index=False)
    bar_plot_per_categories_html = bar_plot_per_categories(df).to_html(
        full_html=False, include_plotlyjs="cdn"
    )
    pie_plot_per_categories_html = pie_plot_per_categories(df).to_html(
        full_html=False, include_plotlyjs="cdn"
    )

    return render_template(
        "dashboard.html",
        title="Resumen general",
        balance_per_month_table=balance_per_month_table,
        last_movements_table=last_movements_table,
        bar_plot_per_categories_html=bar_plot_per_categories_html,
        pie_plot_per_categories_html=pie_plot_per_categories_html,
    )
