"""Module for the Sample Tab 1."""

from nova.trame.view.components import InputField
from nova.trame.view import layouts
from trame.widgets import vuetify3 as vuetify

class SampleTab1:
    """Sample tab 1 view class. Renders text input for username."""

    def __init__(self) -> None:
        self.create_ui()

    def create_ui(self) -> None:
        with layouts.VBoxLayout(classes="ma-2"):  # Overall vertical layout
            InputField(v_model="config.username", label="Username")
            with layouts.HBoxLayout():  # Horizontal layout for first and last name
                InputField(v_model="config.firstName", label="First Name")
                InputField(v_model="config.lastName", label="Last Name")
            vuetify.VCheckbox(label="Remember me")
            vuetify.VSwitch(label="Enable Notifications")