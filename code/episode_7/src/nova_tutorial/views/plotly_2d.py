"""View for the 2d plot."""

from nova.trame.view.components import InputField  # type: ignore
from nova.trame.view.layouts import GridLayout, HBoxLayout  # type: ignore
from trame.widgets import plotly  # type: ignore
from trame.widgets import vuetify3 as vuetify

from nova_tutorial.view_models.visualization import VisualizationViewModel


class Plot2D:
    """View class for the 2d plot."""

    def __init__(self, view_model: VisualizationViewModel) -> None:
        self.view_model = view_model
        self.view_model.config_2d_bind.connect("config_2d")

        self.create_ui()

    def create_ui(self) -> None:
        vuetify.VCardTitle("Plotly")
        with GridLayout(columns=4, classes="mb-2"):
            InputField(v_model="config_2d.plot_type", items="config_2d.plot_type_options", type="select")
            InputField(v_model="config_2d.x_axis", items="config_2d.axis_options", type="select")
            InputField(v_model="config_2d.y_axis", items="config_2d.axis_options", type="select")
            InputField(
                v_model="config_2d.z_axis",
                disabled=("config_2d.is_scatter",),
                items="config_2d.axis_options",
                type="select",
            )

        with HBoxLayout(halign="center", height="50vh"):
            plotly.Figure(v_if="config_2d.plot_data", state_variable_name="config_2d.plot_data")
