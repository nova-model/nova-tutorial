from trame.widgets import vuetify3 as vuetify

from nova.trame.view.components import InputField
from nova_tutorial.app.view_models.main import MainViewModel

class FractalTab:
    def __init__(self, view_model: MainViewModel) -> None:
        self.view_model = view_model
        self.view_model.running_bind.connect("running")
        self.create_ui()

    def create_ui(self) -> None:
        InputField(v_model="config.fractal.fractal_type", classes="mb-2")
        vuetify.VProgressCircular(v_if="running", indeterminate=True)
        vuetify.VBtn(
            "Run Fractal",
            v_else=True,
            click=self.view_model.run_fractal,  # calls the run_fractal_tool method
        )
        vuetify.VImg(src=("config.fractal.image_data",), height="400", width="400")
