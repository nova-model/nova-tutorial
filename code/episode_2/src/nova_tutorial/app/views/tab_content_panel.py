"""Module for the Tab Content panel."""

from nova.trame.view.layouts import VBoxLayout
from trame_server import Server

from ..view_models.main_view_model import MainViewModel
from .sample_tab_1 import SampleTab1
from .sample_tab_2 import SampleTab2


class TabContentPanel:
    """View class to render content for a selected tab."""

    def __init__(self, server: Server, view_model: MainViewModel) -> None:
        self.view_model = view_model
        self.server = server
        self.ctrl = server.controller
        self.create_ui()

    def create_ui(self) -> None:
        with VBoxLayout(v_show="view_state.active_tab == 0", stretch=True):
            SampleTab1()
        with VBoxLayout(v_show="view_state.active_tab == 1", stretch=True):
            SampleTab2()
