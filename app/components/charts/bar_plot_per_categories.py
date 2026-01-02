import plotly.express as px

from app.components.BasePlot import BasePlot
from app.config.config import MONTHS_ORDER
from app.data.processor import amounts_per_month_and_category


class BarPlotPerCategories(BasePlot):
    def create_figure(self):
        data = amounts_per_month_and_category(self.df)
        unique_categories = data.drop_duplicates("category_id").sort_values(
            "category_id"
        )

        color_discrete_map = dict(zip(data["category_id"], data["color"]))
        category_orders = {
            "category_id": [str(i) for i in range(data["category_id"].nunique())],
            "month": MONTHS_ORDER,
        }
        legend_labels = {
            str(row.category_id): f"{row.icon_char} {row.category}"
            for _, row in unique_categories.iterrows()
        }
        icon_map = {
            str(row.category_id): row.icon_char
            for _, row in unique_categories.iterrows()
        }
        category_name_map = {
            str(row.category_id): row.category
            for _, row in unique_categories.iterrows()
        }

        fig = px.bar(
            data,
            x="month",
            y="amount",
            color="category_id",
            title="Gastos por Categoría y Mes",
            labels={"month": "Mes", "amount": "Gastos (€)", "category": "Categoría"},
            color_discrete_map=color_discrete_map,
            category_orders=category_orders,
            hover_name="category",
            hover_data={
                "category_id": False,
                "category": False,
                "amount": ":.2f",
                "month": False,
            },
        )

        for trace in fig.data:
            category_id = trace.name
            if category_id in legend_labels:
                icon = icon_map.get(category_id, "")
                category_name = category_name_map.get(category_id, "")
                trace.name = legend_labels[category_id]
                trace.hovertemplate = f"<b>{icon} {category_name}</b><br>Gastos (€): %{{y:.2f}}<extra></extra>"
                trace.text = [f"{icon} {category_name}" for _ in trace.y]
                trace.textposition = "outside"
                trace.textfont = dict(size=10)

        fig.update_layout(
            legend_title_text="Categorías",
            showlegend=True,
        )

        return fig
