import logging

import pandas as pd
from sqlalchemy import create_engine

from app.config.config import GOOGLE_DRIVE_URL_TEMPLATE, SQLALCHEMY_DATABASE_URI


def sync_transactions():
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

    engine = create_engine(SQLALCHEMY_DATABASE_URI)
    categories = pd.read_sql(
        "SELECT * FROM categories",
        engine,
        parse_dates=["date_created", "date_modified"],
    )
    trips = pd.read_sql(
        "SELECT * FROM trips",
        engine,
        parse_dates=["date_start", "date_end", "date_created", "date_modified"],
    )
    types = pd.read_sql(
        "SELECT * FROM types",
        engine,
        parse_dates=["date_created", "date_modified"],
    )

    df["trip_id"] = df.merge(trips, how="left", left_on="trip", right_on="name")[
        "id"
    ].astype("Int64")
    # TODO catch error when missing category
    df["category_id"] = df.merge(
        categories, how="left", left_on="category", right_on="name"
    )["id"].astype("Int64")
    df["type_id"] = df.merge(types, how="left", left_on="type", right_on="name")["id"]
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

    # TODO not replace entire database, only update new fields
    df.to_sql("transactions", engine, index=False, if_exists="replace")

    logger.info(f"Successfully inserted {len(df)} rows into the 'transactions' table")
    return


if __name__ == "__main__":
    sync_transactions()
