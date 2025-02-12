"""Module for the Sample Tab 1."""

from nova.trame.view.components import InputField, RemoteFileInput


class SampleTab1:
    """Sample tab 1 view class. Renders text input for username."""

    def __init__(self) -> None:
        self.create_ui()

    def create_ui(self) -> None:
        RemoteFileInput(v_model="file", base_paths=["/HFIR", "/SNS"])
        InputField(v_model="config.username")
