from abc import ABC, abstractmethod


class BasePlot(ABC):
    DEFAULT_FONT = dict(family="SauceCodeProNF, monospace")
    DEFAULT_HOVER_FONT = dict(
        family="SauceCodeProNF, monospace", size=12, color="black"
    )

    def __init__(self, df):
        self.df = df
        self._fig = None

    @abstractmethod
    def create_figure(self):
        pass

    @property
    def fig(self):
        if self._fig is None:
            self._fig = self.create_figure()
            self._apply_common_styling()
        return self._fig

    def _apply_common_styling(self):
        self._fig.update_layout(font=self.DEFAULT_FONT)
        self._fig.update_traces(hoverlabel=dict(font=self.DEFAULT_HOVER_FONT))

    def to_html(self, full_html=False, include_plotlyjs="cdn", **kwargs):
        return self.fig.to_html(
            full_html=full_html, include_plotlyjs=include_plotlyjs, **kwargs
        )

    def show(self):
        self.fig.show()

    def write_html(self, file_path):
        self.fig.write_html(file_path)

    def update_layout(self, **kwargs):
        self.fig.update_layout(**kwargs)
        return self
