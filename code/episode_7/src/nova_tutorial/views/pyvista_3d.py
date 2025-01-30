"""View for the 3d plot using PyVista."""

from functools import partial
from typing import Optional

import pyvista as pv  # type: ignore
from nova.trame.view.components import InputField  # type: ignore
from nova.trame.view.layouts import GridLayout, HBoxLayout  # type: ignore
from pyvista.trame.ui import plotter_ui  # type: ignore
from trame.widgets import vuetify3 as vuetify  # type: ignore

from nova_tutorial.view_models.visualization import VisualizationViewModel


class PyVistaPlot:
    """View class for the 3d plot using PyVista."""

    def __init__(self, view_model: VisualizationViewModel) -> None:
        self.view_model = view_model
        self.view_model.config_pyvista_bind.connect("config_pyvista")

        self.plotter: Optional[pv.Plotter] = None

        self.create_plotter()
        self.create_ui()

    def create_plotter(self) -> None:
        self.plotter = pv.Plotter(off_screen=True)

    def create_ui(self) -> None:
        vuetify.VCardTitle("PyVista")
        with GridLayout(columns=5, classes="mb-2", valign="center"):
            InputField(
                v_model="config_pyvista.colormap", column_span=2, items="config_pyvista.colormap_options", type="select"
            )
            InputField(
                v_model="config_pyvista.opacity", column_span=2, items="config_pyvista.opacity_options", type="select"
            )
            vuetify.VBtn("Render", click=partial(self.view_model.render_pyvista, self.plotter))

        with HBoxLayout(halign="center", height="50vh"):
            plotter_ui(self.plotter)
