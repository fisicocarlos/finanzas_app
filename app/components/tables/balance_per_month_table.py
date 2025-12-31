from app.data.processor import balance_per_month


def balance_per_month_table(df):
    return balance_per_month(df).to_html(index_names=False)
