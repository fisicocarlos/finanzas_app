from app.data.processor import trips


def trips_table():
    return trips().to_html(index=False)
