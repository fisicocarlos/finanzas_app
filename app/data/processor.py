import pandas as pd

from app.config.config import TRANSLATIONS
from app.data.drive_reader import load_categories


def grouped_movements(df):
    grouped = df.groupby(
        ["type", "trip_id", "category_id", pd.Grouper(key="date", freq="ME")]
    )[["amount"]].sum()
    return grouped


def balance_per_month(df, lang="es"):
    df["month"] = df["date"].dt.to_period("M")
    balance = pd.pivot_table(
        df, values="amount", index="month", columns="type", aggfunc="sum", fill_value=0
    )
    balance["total"] = balance.get("expense", 0) + balance.get("income", 0)
    # Language support
    translations = {
        k: v.capitalize() for k, v in TRANSLATIONS.get(lang, TRANSLATIONS["en"]).items()
    }
    balance.rename(columns=translations, inplace=True)
    balance.rename_axis(
        index="Mes" if lang == "es" else "month",
        columns="Tipo" if lang == "es" else "type",
        inplace=True,
    )
    balance.index = balance.index.strftime("%B").str.capitalize()
    return balance


def last_movements(df, n=5, lang="es"):
    lasts_movements = df[["description", "amount"]].tail(n)
    translations = {
        k: v.capitalize() for k, v in TRANSLATIONS.get(lang, TRANSLATIONS["en"]).items()
    }
    lasts_movements.rename(columns=translations, inplace=True)
    return lasts_movements


def amounts_per_month_and_category(df):
    grouped_df = (
        df[df["type"] == "expense"]
        .groupby(["category_id", pd.Grouper(key="date", freq="ME")], as_index=False)[
            ["amount"]
        ]
        .sum()
        .sort_values(["date", "category_id"], ignore_index=True)
    )
    categories = load_categories()
    amounts = pd.merge(
        grouped_df,
        categories,
        how="left",
        left_on="category_id",
        right_on="id",
    ).rename(columns={"name": "category"})
    amounts["amount"] = -amounts["amount"]
    amounts["month"] = amounts["date"].dt.strftime("%B").str.capitalize()
    return amounts
