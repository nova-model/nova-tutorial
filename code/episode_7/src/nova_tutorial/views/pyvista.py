"""View for the 3d plot using PyVista."""

from typing import Any, Optional

import pyvista as pv
from nova.trame.view.components import InputField
from nova.trame.view.layouts import GridLayout, HBoxLayout
from pyvista.trame.ui import plotter_ui
from trame.widgets import vuetify3 as vuetify

from nova_tutorial.view_models.visualization import VisualizationViewModel


class PyVistaView:
    """View class for the 3d plot using PyVista."""

    def __init__(self, view_model: VisualizationViewModel) -> None:
        self.view_model = view_model
        self.view_model.pyvista_config_bind.connect("pyvista_config")

        self.plotter: Optional[pv.Plotter] = None

        self.create_plotter()
        self.create_ui()

    def create_plotter(self) -> None:
        self.plotter = pv.Plotter(off_screen=True)

    def create_ui(self) -> None:
        vuetify.VCardTitle("PyVista")
        with GridLayout(columns=5, classes="mb-2", valign="center"):
            InputField(
                v_model="pyvista_config.colormap", column_span=2, items="pyvista_config.colormap_options", type="select"
            )
            InputField(
                v_model="pyvista_config.opacity", column_span=2, items="pyvista_config.opacity_options", type="select"
            )
            vuetify.VBtn("Render", click=self.update)
        with HBoxLayout(halign="center", height="50vh"):
            plotter_ui(self.plotter)

    def update(self, _: Any = None) -> None:
        if self.plotter:
            self.view_model.render_pyvista(self.plotter)
