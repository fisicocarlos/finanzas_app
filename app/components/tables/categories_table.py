from app.data.processor import categories


def categories_table():
    return categories().to_html()
