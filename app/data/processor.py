import pandas as pd

def gastos_mensuales(df):
    gastos_mensuales = (
        df[df['tipo'] == "gasto"]
        .groupby(['month', 'categoria'], as_index=False, observed=True)['cantidad']
        .sum()
        .sort_values(["month", "cantidad"], ignore_index=True)
    )
    gastos_mensuales['cantidad'] = - gastos_mensuales['cantidad']
    gastos_mensuales['month'] = gastos_mensuales['month'].dt.strftime("%b").str.capitalize()

    totales = (
        gastos_mensuales
        .groupby("categoria", as_index=False, observed=True)["cantidad"]
        .sum()
        .sort_values("cantidad", ascending=False)  # Ascendente → las más grandes abajo
    )
    orden_categorias = totales["categoria"].tolist()
    gastos_mensuales["categoria"] = pd.Categorical(
        gastos_mensuales["categoria"],
        categories=orden_categorias,
        ordered=True
    )
    return gastos_mensuales
