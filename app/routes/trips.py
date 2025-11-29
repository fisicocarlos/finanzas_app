from flask import Blueprint, render_template

from app.data.processor import trips_table

bp = Blueprint("trips", __name__, url_prefix="/trips")


@bp.route("/")
def index():
    trips_table_html = trips_table().to_html(index=False)
    return render_template(
        "trips.html", title="Gastos por viaje", trips_table_html=trips_table_html
    )
