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
            InputField(v_model="fractal.fractal_type", type="select")
        with VBoxLayout(halign="center", valign="center", stretch=True):
            vuetify.VProgressCircular(v_if="view_state.running", indeterminate=True)
            vuetify.VImg(v_else=True, src=("fractal.image_data",), classes="h-100 w-100")
