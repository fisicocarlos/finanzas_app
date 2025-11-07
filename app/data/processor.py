import pandas as pd

from app.config.config import TRANSLATIONS


def grouped_movements(df):
    grouped = df.groupby(
        ["type", "trip_id", "category_id", pd.Grouper(key="date", freq="ME")]
    )["amount"].sum()

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


def balance_last_month(df):
    return balance_per_month(df[df["date"] > pd.Timestamp.today().replace(day=1)])
