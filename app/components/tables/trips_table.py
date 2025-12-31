from app.data.processor import total_amount_per_trip


def trips_table():
    return (
        total_amount_per_trip()
        .rename(
            columns={
                "trip_name": "Nombre",
                "date_start": "Inicio",
                "date_end": "Fin",
                "total_amount": "Total gastado",
            }
        )
        .to_html(index=False)
    )
