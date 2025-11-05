from flask import Blueprint, render_template

bp = Blueprint("viajes", __name__, url_prefix="/viajes")

@bp.route("/")
def index():
    return render_template("viajes.html", title="Gastos por viaje")
