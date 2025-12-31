from app.data.processor import last_movements


def last_movements_table(df, n=5):
    return last_movements(df, n).to_html(index=False)
