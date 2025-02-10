"""Main file."""

import logging

from nova.mvvm.trame_binding import TrameBinding
from nova.trame import ThemedApp
from trame.app import get_server
from nova.trame.view.components import InputField
from trame.widgets import vuetify3 as vuetify

from ..mvvm_factory import create_viewmodels
from ..view_models.main import MainViewModel

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class MainApp(ThemedApp):
    """Main application view class. Renders all UI elements on the mainn page."""

    def __init__(self) -> None:
        super().__init__()
        self.server = get_server(None, client_type="vue3")
        binding = TrameBinding(self.server.state)
        self.server.state.trame__title = "Trame With Pydantic"
        self.view_models = create_viewmodels(binding)
        self.view_model: MainViewModel = self.view_models["main"]
        self.view_model.settings_bind.connect("settings")
        self.create_ui()

    def create_ui(self) -> None:
        self.state.trame__title = "Trame With Pydantic"

        with super().create_ui() as layout:
            layout.toolbar_title.set_text("Trame With Pydantic")
            with layout.pre_content:
                pass
            with layout.content:
                with vuetify.VRow(align="center", classes="mt-4"):
                    InputField(v_model="settings.port")
            with layout.post_content:
                pass
            return layout
