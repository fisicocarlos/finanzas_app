import pandas as pd
import plotly.express as px

from app.config.config import MONTHS_ORDER
from app.data.processor import amounts_per_month_and_category


def bar_plot_per_categories(df):
    data = amounts_per_month_and_category(df)

    color_discrete_map = dict(zip(data["category"], data["color"]))
    category_orders = {
        "category_id": [str(i) for i in range(data["category_id"].nunique())],
        "month": MONTHS_ORDER,
    }

    fig = px.bar(
        data,
        x="month",
        y="amount",
        color="category_id",
        text_auto=True,
        title="Gastos",
        labels={"month": "Mes", "amount": "Gastos", "category": "Categoría"},
        color_discrete_map=color_discrete_map,
        category_orders=category_orders,
        hover_name="category",
        hover_data={
            "category_id": False,
            "category": False,
            "amount": ":.0f",
            "month": False,
        },
    )
    legend_labels = {
        str(row.category_id): f"{row.icon_char} {row.category}"
        for _, row in data.drop_duplicates("category_id").iterrows()
    }
    fig.for_each_trace(lambda t: t.update(name=legend_labels.get(t.name, t.name)))
    fig.update_layout(legend_title_text="Categorías")
    fig.update_layout(font=dict(family="SauceCodeProNF, monospace"))
    return fig


def pie_plot_per_categories(df, start=pd.Timestamp.today().replace(day=1)):
    data = amounts_per_month_and_category(df)
    filtered_data = data[data["date"] >= start]
    color_map = dict(zip(filtered_data["category"], filtered_data["color"]))

    legend_labels = {
        str(row.category_id): f"{row.icon_char} {row.category}"
        for _, row in data.drop_duplicates("category_id").iterrows()
    }

    fig = px.pie(
        filtered_data,
        values="amount",
        names="category",
        color="category",
        color_discrete_map=color_map,
        labels={"category": "Categoría", "amount": "Cantidad"},
        title=start.strftime("%B").capitalize(),
    )

    fig.update_layout(
        font=dict(family="SauceCodeProNF, monospace"),
        legend_title_text="Categorías",
        showlegend=True,
    )

    fig.update_traces(
        texttemplate="%{customdata[0]} %{value:.0f} €",
        customdata=filtered_data[["icon_char"]].values,
        textposition="inside",
        textfont_size=14,
        hovertemplate="<b>%{label}</b>%{customdata[0]}<br>Importe: €%{value:.2f}<br>Porcentaje: %{percent}<extra></extra>",
        hoverlabel=dict(
            font=dict(family="SauceCodeProNF, monospace", size=12, color="black")
        ),
    )

    fig.for_each_trace(lambda t: t.update(name=legend_labels.get(t.name, t.name)))

    return fig
