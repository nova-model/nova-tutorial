"""Main file."""

import logging

from nova.mvvm.trame_binding import TrameBinding
from nova.trame import ThemedApp
from nova.trame.view import layouts
from trame.app import get_server
from trame.widgets import vuetify3 as vuetify

from ..mvvm_factory import create_viewmodels
from ..view_models.main import MainViewModel
from .tab_content_panel import TabContentPanel
from .tabs_panel import TabsPanel

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class MainApp(ThemedApp):
    """Main application view class. Calls rendering of nested UI elements."""

    def __init__(self) -> None:
        super().__init__()
        self.server = get_server(None, client_type="vue3")
        binding = TrameBinding(self.server.state)
        self.view_models = create_viewmodels(binding)
        self.view_model: MainViewModel = self.view_models["main"]
        self.create_ui()

    def create_ui(self) -> None:
        self.state.trame__title = "Fractal Tool GUI"

        with super().create_ui() as layout:
            layout.toolbar_title.set_text("Fractal Tool GUI")
            with layout.pre_content:
                TabsPanel(self.view_models["main"])
            with layout.content:
                TabContentPanel(
                    self.server,
                    self.view_models["main"],
                )
            with layout.post_content:
                with layouts.HBoxLayout(classes="my-2", halign="center"):
                    vuetify.VBtn(
                        "Run Fractal",
                        click=self.view_model.run_fractal,  # calls the run_fractal_tool method
                    )
            return layout
