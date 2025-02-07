"""Module for the Tab Content panel."""

from trame.widgets import vuetify3 as vuetify
from trame_server import Server

from ..view_models.main import MainViewModel
from ..views.plotly import PlotlyView
from ..views.pyvista import PyVistaView
from ..views.vtk import VTKView


class TabContentPanel:
    """View class to render content for a selected tab."""

    def __init__(self, server: Server, view_model: MainViewModel) -> None:
        self.view_model = view_model
        self.server = server
        self.ctrl = server.controller
        self.create_ui()

    def create_ui(self) -> None:
        with vuetify.VForm(ref="form") as self.f:
            with vuetify.VContainer(classes="pa-0", fluid=True):
                with vuetify.VCard():
                    with vuetify.VWindow(v_model="active_tab"):
                        with vuetify.VWindowItem(value=1):
                            PlotlyView(self.view_model)
                        with vuetify.VWindowItem(value=2):
                            PyVistaView(self.view_model)
                        with vuetify.VWindowItem(value=3):
                            VTKView(self.view_model)
