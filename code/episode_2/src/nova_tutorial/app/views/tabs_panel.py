"""Module for the Tab panel."""

from trame.widgets import client
from trame.widgets import vuetify3 as vuetify

from ..view_models.main_view_model import MainViewModel


class TabsPanel:
    """View class to render tabs."""

    def __init__(self, view_model: MainViewModel):
        self.view_model = view_model
        self.view_model.config_bind.connect("config")
        self.view_model.view_state_bind.connect("view_state")
        self.create_ui()

    def create_ui(self) -> None:
        with client.DeepReactive("view_state"):
            with vuetify.VTabs(v_model="view_state.active_tab", classes="pl-5"):
                vuetify.VTab("Sample Tab 1", value=0)
                vuetify.VTab("Sample Tab 2", value=1)
