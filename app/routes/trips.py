from flask import Blueprint, render_template

from app.components.tables import trips_table

bp = Blueprint("trips", __name__, url_prefix="/trips")


@bp.route("/")
def index():
    return render_template(
        "trips.html", title="Gastos por viaje", trips_table_html=trips_table()
    )
