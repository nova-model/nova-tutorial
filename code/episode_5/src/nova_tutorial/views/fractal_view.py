from nova.mvvm.trame_binding import TrameBinding
from nova.trame import ThemedApp
from nova.trame.view import layouts
from trame.app import get_server
from trame.widgets import vuetify3 as vuetify
from nova_tutorial.view_models.fractal_view_model import FractalViewModel

class FractalApp(ThemedApp): # Inherits from nova.trame.ThemedApp for consistent styling
    def __init__(self) -> None:
        super().__init__()
        self.server = get_server(None, client_type="vue3")
        self.fractal_vm = FractalViewModel(TrameBinding(self.server.state))
        self.fractal_vm.fractal_type_bind.connect("fractal_type")
        self.fractal_vm.message_bind.connect("fractal_message")
        self.fractal_vm.job_status_bind.connect("job_status")
        #self.fractal_vm.init_view()
        self.create_ui()

    def create_ui(self) -> None:
        self.state.trame__title = "NOVA Tutorial"
        with super().create_ui() as layout:
            with layout.content:
                with layouts.VBoxLayout(classes="ma-2"):
                    with vuetify.VCard(classes="pa-2"):
                        with vuetify.VRadioGroup(
                            v_model=("fractal_type"),
                            classes="mb-2",
                            #update_modelValue=self.fractal_vm.set_fractal_type(model_value)
                        ):
                            vuetify.VRadio(label="Mandelbrot", value="mandelbrot")
                            vuetify.VRadio(label="Julia", value="julia")
                            vuetify.VRadio(label="Random", value="random")
                            vuetify.VRadio(label="Markus", value="markus")
                        vuetify.VBtn(
                            "Run Fractal Tool",
                            v_model="job_status",
                            click=self.fractal_vm.run_fractal_tool,
                            #disabled=("job_status['fractal'] == 'Starting'"),
                            classes="mb-2"
                        )
                        vuetify.VCardText(v_model=("fractal_message"))
            return layout