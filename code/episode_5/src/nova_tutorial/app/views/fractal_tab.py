from trame.widgets import vuetify3 as vuetify

from nova.trame.view.components import InputField
from nova_tutorial.app.view_models.main import MainViewModel
from nova.trame.view import layouts

class FractalTab:

    def __init__(self, view_model: MainViewModel) -> None:
        self.view_model = view_model
        self.create_ui()

    def create_ui(self) -> None:
        with layouts.VBoxLayout(classes="ma-4"):
            with vuetify.VCard(classes="pa-4"):
                InputField(
                    v_model=("config.fractal.fractal_type", "mandelbrot"),
                    label="Fractal Type",
                )
                vuetify.VBtn(
                    "Run Fractal",
                    click=self.view_model.run_fractal,
                    classes="mt-2",
                )
                vuetify.VCardText(v_text="config.status_message", classes="mt-2")