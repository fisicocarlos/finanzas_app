import pandas as pd
import plotly.express as px


def gastos_mensuales(df):
    gastos_mensuales = (
        df[df["tipo"] == "gasto"]
        .groupby(["month", "categoria"], as_index=False, observed=True)["cantidad"]
        .sum()
        .sort_values(["month", "cantidad"], ignore_index=True)
    )
    gastos_mensuales["cantidad"] = -gastos_mensuales["cantidad"]
    gastos_mensuales["month"] = (
        gastos_mensuales["month"].dt.strftime("%b").str.capitalize()
    )

    totales = (
        gastos_mensuales.groupby("categoria", as_index=False, observed=True)["cantidad"]
        .sum()
        .sort_values("cantidad", ascending=False)
    )
    orden_categorias = totales["categoria"].tolist()
    gastos_mensuales["categoria"] = pd.Categorical(
        gastos_mensuales["categoria"], categories=orden_categorias, ordered=True
    )

    fig = px.bar(
        gastos_mensuales,
        x="month",
        y="cantidad",
        color="categoria",
        text_auto=True,
        title="Gastos",
        labels={"month": "Mes", "cantidad": "Gastos", "categoria": "Categoria"},
    )
    return fig.to_html(full_html=False, include_plotlyjs="cdn")
