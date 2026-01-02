import pandas as pd
import plotly.express as px

from app.components.BasePlot import BasePlot
from app.data.processor import amounts_per_month_and_category


class PiePlotPerCategories(BasePlot):
    def __init__(self, df, start=None):
        super().__init__(df)
        self.start = start or pd.Timestamp.today().replace(day=1)

    def create_figure(self):
        data = amounts_per_month_and_category(self.df)
        filtered_data = data[data["date"] >= self.start]

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
            title=self.start.strftime("%B").capitalize(),
            width=600,
            height=400,
        )

        fig.update_layout(
            legend_title_text="Categorías",
            showlegend=True,
        )

        fig.update_traces(
            texttemplate="%{customdata[0]} %{value:.0f} €",
            customdata=filtered_data[["icon_char"]].values,
            textposition="inside",
            textfont_size=14,
            hovertemplate="<b>%{label}</b>%{customdata[0]}<br>Importe: €%{value:.2f}<br>Porcentaje: %{percent}<extra></extra>",
        )

        fig.for_each_trace(lambda t: t.update(name=legend_labels.get(t.name, t.name)))

        return fig
