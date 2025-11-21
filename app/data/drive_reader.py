import logging

import pandas as pd

from app.config.config import GOOGLE_DRIVE_URL_TEMPLATE
from app.data.DatabaseManager import PostgresDB


def load_data():
    logger = logging.getLogger(__name__)

    columns = ["date", "description", "category", "amount", "notes", "trip"]
    gastos = pd.read_csv(
        GOOGLE_DRIVE_URL_TEMPLATE.format(gid=0),
        names=columns,
        header=0,
        parse_dates=["date"],
        date_format="%d/%m/%Y",
    ).dropna(how="all")
    gastos["type"] = "expense"

    ingresos = pd.read_csv(
        GOOGLE_DRIVE_URL_TEMPLATE.format(gid=476570121),
        names=columns,
        header=0,
        parse_dates=["date"],
        date_format="%d/%m/%Y",
    ).dropna(how="all")
    ingresos["type"] = "income"
    df = pd.concat([gastos, ingresos]).sort_values("date").reset_index()
    df["trip"] = df["trip"].fillna("not-a-trip")
    logger.info("Read data from google drive")

    # Join with categories and trips
    with PostgresDB() as db:
        categories = db.fetch_table("categories")
        trips = db.fetch_table("trips")

    df["trip_id"] = df.merge(trips, how="left", left_on="trip", right_on="name")["id"]
    df["category_id"] = df.merge(
        categories, how="left", left_on="category", right_on="name"
    )["id"]
    if logger.isEnabledFor(logging.DEBUG):
        missing_categories = df.loc[df["category_id"].isna(), "category"].unique()
        if len(missing_categories):
            logger.warning(
                "Categories without matches found: %s",
                ", ".join(map(str, missing_categories)),
            )

    return df[
        [
            "date",
            "description",
            "type",
            "category",
            "category_id",
            "amount",
            "trip",
            "trip_id",
            "notes",
        ]
    ]
