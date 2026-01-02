"""Module for the Sample Tab 2."""

from nova.trame.view.components import InputField
from nova.trame.view.layouts import VBoxLayout


class SampleTab2:
    """Sample tab 2 view class. Renders text input for user password."""

    def __init__(self) -> None:
        self.create_ui()

    def create_ui(self) -> None:
        with VBoxLayout():
            InputField(v_model="config.password")
