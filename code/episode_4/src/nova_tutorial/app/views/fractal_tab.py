from trame.widgets import vuetify3 as vuetify

from nova.trame.view.components import InputField
from nova.trame.view.layouts import VBoxLayout
from nova_tutorial.app.view_models.main_view_model import MainViewModel


class FractalTab:
    def __init__(self, view_model: MainViewModel) -> None:
        self.view_model = view_model
        self.view_model.fractal_bind.connect("fractal")
        self.create_ui()

    def create_ui(self) -> None:
        with VBoxLayout():
            InputField(v_model="fractal.fractal_type")
        with VBoxLayout(classes="mb-2", halign="start"):
            vuetify.VBtn("Run Fractal", click=self.view_model.run_fractal)
        with VBoxLayout(stretch=True):
            vuetify.VImg(src=("fractal.image_data",), classes="h-100 w-100")
