"""View for Plotly."""

import plotly.graph_objects as go
from nova.trame.view.components import InputField
from nova.trame.view.layouts import GridLayout, HBoxLayout
from trame.widgets import plotly

from ..view_models.main import MainViewModel

class PlotlyView:
    """View class for Plotly."""

    def __init__(self, view_model: MainViewModel) -> None:
        self.view_model = view_model
        self.view_model.plotly_config_bind.connect("plotly_config")
        self.view_model.plotly_figure_bind.connect(self.update_figure)

        self.create_ui()

        self.view_model.update_plotly_figure()

    def create_ui(self) -> None:
        with GridLayout(columns=4, classes="mb-2"):
            InputField(v_model="plotly_config.plot_type", type="select")
            InputField(v_model="plotly_config.x_axis", type="select")
            InputField(v_model="plotly_config.y_axis", type="select")
            InputField(v_model="plotly_config.z_axis", disabled=("plotly_config.is_not_heatmap",), type="select")

        with HBoxLayout(halign="center", height="50vh"):
            self.figure = plotly.Figure()

    def update_figure(self, figure: go.Figure) -> None:
        self.figure.update(figure)
        self.figure.state.flush()  # This is necessary if you call update asynchronously.
