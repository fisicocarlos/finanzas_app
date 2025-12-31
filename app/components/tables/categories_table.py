from app.data.processor import all_categories


def categories_table():
    return (
        all_categories()
        .rename(
            columns={
                "category_name": "Categoría",
            }
        )
        .style.apply(
            lambda row: [f"background-color: {row['color']}"] * len(row), axis=1
        )
        .to_html()
    )
