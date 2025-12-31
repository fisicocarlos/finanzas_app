import pandas as pd
from flask import Blueprint, render_template

from app import db
from app.components.charts import bar_plot_per_categories, pie_plot_per_categories
from app.data.processor import balance_per_month, last_movements
from app.models.categories import Category
from app.models.transactions import Transaction
from app.models.trips import Trip
from app.models.types import Type

bp = Blueprint("dashboard", __name__, url_prefix="/")


@bp.route("/")
def index():
    query = (
        db.session.query(
            Transaction.date,
            Transaction.description,
            Type.name.label("type"),
            Category.name.label("category"),
            Category.id.label("category_id"),
            Transaction.amount,
            Trip.name.label("trip"),
            Trip.id.label("trip_id"),
            Transaction.notes,
        )
        .outerjoin(Type, Transaction.type_id == Type.id)
        .outerjoin(Category, Transaction.category_id == Category.id)
        .outerjoin(Trip, Transaction.trip_id == Trip.id)
        .order_by(Transaction.date.desc())
    )
    df = pd.read_sql(query.statement, db.engine, parse_dates=["date"])

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
