from flask import Blueprint, render_template

from app.data.DatabaseManager import PostgresDB
from app.data.processor import balance_per_month, last_movements
from app.data.plots import bar_plot_per_categories, pie_plot_per_categories

bp = Blueprint("dashboard", __name__, url_prefix="/")


@bp.route("/")
def index():
    with PostgresDB() as db:
        df = db.fetch(
            """SELECT
                T.DATE,
                T.DESCRIPTION,
                TY.NAME AS TYPE,
                C.NAME AS CATEGORY,
                C.ID AS CATEGORY_ID,
                T.AMOUNT,
                TRIPS.name AS trip,
                trips.id as trip_id,
                T.NOTES
                FROM
                TRANSACTIONS T
                LEFT JOIN TYPES TY ON T.TYPE_ID = TY.ID
                LEFT JOIN CATEGORIES C ON T.CATEGORY_ID = C.ID
                LEFT JOIN TRIPS ON T.TRIP_ID = TRIPS.ID;""",
            parse_dates=["date"],
        )

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
