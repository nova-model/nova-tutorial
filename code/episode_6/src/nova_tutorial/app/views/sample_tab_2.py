"""Module for the Sample Tab 2."""

from nova.trame.view.components import InputField
from nova.trame.view import layouts
from trame.widgets import vuetify3 as vuetify


class SampleTab2:
    """Sample tab 2 view class. Renders text input for user password."""

    def __init__(self) -> None:
        self.create_ui()

    def create_ui(self) -> None:
        with layouts.VBoxLayout(classes="ma-2"): # Parent vertical layout
            with layouts.HBoxLayout():  # Horizontal layout for email and phone
                InputField(v_model="config.sample_tab2.email", label="Email", type="email")
                InputField(v_model="config.sample_tab2.phoneNumber", label="Phone Number", type="tel")
            with layouts.GridLayout(columns=2): # Two column grid layout for remaining fields
                vuetify.VSlider(label="Volume")
                with layouts.VBoxLayout(classes="ma-2"):  # Overall vertical layout
                    vuetify.VLabel("Item 1", classes="bg-primary h-100 w-100 justify-center")
                    vuetify.VLabel("Item 2", classes="bg-secondary h-100 w-100 justify-center")
                InputField(v_model="config.address", label="Address")
                InputField(v_model="config.comments", label="Comments")