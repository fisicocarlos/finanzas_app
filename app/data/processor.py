import pandas as pd


def grouped_movements(df):
    grouped = df.groupby(
        ["type", "trip_id", "category_id", pd.Grouper(key="date", freq="ME")]
    )["amount"].sum()

    return grouped


def balance_per_month(df):
    balance = (
        df.groupby(["type", pd.Grouper(key="date", freq="ME")])["amount"]
        .sum()
        .unstack(fill_value=0)
    )
    balance.loc["total"] = balance.sum()
    balance.columns = balance.columns.strftime("%B").str.capitalize()
    return balance


def balance_last_month(df):
    return balance_per_month(df[df["date"] > pd.Timestamp.today().replace(day=1)])
