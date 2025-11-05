import pandas as pd

from app.config.config import GOOGLE_DRIVE_URL_TEMPLATE, logger


def load_data():
    columns = ['fecha', 'descripcion', 'categoria', 'cantidad', 'notas', 'viaje']
    gastos = pd.read_csv(
        GOOGLE_DRIVE_URL_TEMPLATE.format(gid=0),
        names=columns,
        header=0,
        parse_dates=["fecha"],
        date_format="%d/%m/%Y"
    ).dropna(how="all")
    gastos['tipo'] = "gasto"

    ingresos = pd.read_csv(
        GOOGLE_DRIVE_URL_TEMPLATE.format(gid=476570121),
        names=columns,
        header=0,
        parse_dates=["fecha"],
        date_format="%d/%m/%Y"
    ).dropna(how="all")
    ingresos['tipo'] = "ingreso"
    df = pd.concat([gastos, ingresos]).sort_values("fecha")

    orden_categorias = (
        df
        .groupby("categoria")['cantidad']
        .apply(lambda x: x.abs().sum())
        .sort_values(ascending=False)
        .index.to_list()

    )
    df['categoria'] = pd.Categorical(
        df['categoria'],
        categories=orden_categorias,
        ordered=True
    )

    df['month'] = df['fecha'].dt.to_period('M')
    df['year'] = df['fecha'].dt.to_period('Y')

    logger.info("Leidos datos desde google drive")
    return df
