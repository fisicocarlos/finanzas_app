import logging

import numpy as np
import pandas as pd

from app.config.config import GOOGLE_DRIVE_URL_TEMPLATE
from app.data.DatabaseManager import PostgresDB


def fetch_and_store_transactions():
    """
    Fetches transaction data from Google Drive CSV files, processes and merges it with categories and trips from the database,
    and upserts the resulting transactions into the 'transactions' table in the database.

    The function reads expenses and income data, matches categories and trips, and logs any missing categories.
    No parameters are required, and nothing is returned.
    """
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
    logger.info("Read data from google drive")

    # Join with categories and trips
    with PostgresDB() as db:
        categories = db.fetch_table("categories")
        trips = db.fetch_table("trips")
        types = db.fetch_table("types")

    df["trip_id"] = df.merge(trips, how="left", left_on="trip", right_on="name")[
        "id"
    ].replace({np.nan: None})
    df["category_id"] = df.merge(
        categories, how="left", left_on="category", right_on="name"
    )["id"].astype("int")
    df["type_id"] = df.merge(types, how="left", left_on="type", right_on="name")[
        "id"
    ].astype("int")
    if logger.isEnabledFor(logging.DEBUG):
        missing_categories = df.loc[df["category_id"].isna(), "category"].unique()
        if len(missing_categories):
            logger.warning(
                "Categories without matches found: %s",
                ", ".join(map(str, missing_categories)),
            )

    df = df[
        ["date", "description", "type_id", "amount", "category_id", "trip_id", "notes"]
    ]
    df = df.where(pd.notna(df), None)
    with PostgresDB() as db:
        db.upsert_df(
            df,
            "transactions",
            ["date", "description"],
            ["category_id", "type_id", "amount", "trip_id", "notes"],
        )
    logger.info(f"Successfully inserted {len(df)} rows into the 'transactions' table")
    return
