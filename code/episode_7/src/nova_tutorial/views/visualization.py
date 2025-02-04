"""View for the visualization examples."""

from typing import Any

from nova.mvvm.trame_binding import TrameBinding
from nova.trame import ThemedApp
from trame.app import get_server
from trame.widgets import vuetify3 as vuetify

from nova_tutorial.view_models.visualization import VisualizationViewModel
from nova_tutorial.views.plotly import PlotlyView
from nova_tutorial.views.pyvista import PyVistaView
from nova_tutorial.views.vtk import VTKView


class VisualizationApp(ThemedApp):  # Inherits from nova.trame.ThemedApp for consistent styling
    """View class for the visualization examples."""

    def __init__(self) -> None:
        super().__init__()
        self.server = get_server(None, client_type="vue3")
        self.ctrl = self.server.controller

        self.view_model = VisualizationViewModel(TrameBinding(self.server.state))
        self.view_model.controls_bind.connect("controls")

        self.create_ui()

        # This makes the loading of the initial Trame state asynchronous, which is useful for improving the launch time
        # of the application.
        self.ctrl.on_server_ready.add(self.server_ready)

    def server_ready(self, **_kwargs: Any) -> None:
        self.view_model.init_view()

    def create_ui(self) -> None:
        self.state.trame__title = "NOVA Tutorial"
        with super().create_ui() as layout:
            with layout.pre_content:
                with vuetify.VTabs(
                    v_model="controls.active_tab", classes="pl-4", update_modelValue="flushState('controls');"
                ):
                    vuetify.VTab("Plotly", value=0)
                    vuetify.VTab("PyVista", value=1)
                    vuetify.VTab("VTK", value=2)

            with layout.content:
                with vuetify.VCard():
                    with vuetify.VTabsWindow(v_model="controls.active_tab"):
                        with vuetify.VTabsWindowItem(value=0):
                            PlotlyView(self.view_model)
                        with vuetify.VTabsWindowItem(value=1):
                            PyVistaView(self.view_model)
                        with vuetify.VTabsWindowItem(value=2):
                            VTKView(self.view_model)

            layout.post_content.classes += "mb-4"

            return layout
