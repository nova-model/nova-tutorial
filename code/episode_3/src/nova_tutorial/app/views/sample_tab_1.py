"""Module for the Sample Tab 1."""

from nova.trame.view.components import InputField


class SampleTab1:
    """Sample tab 1 view class. Renders text input for username."""

    def __init__(self) -> None:
        self.create_ui()

    def create_ui(self) -> None:
        InputField(v_model="config.username")
