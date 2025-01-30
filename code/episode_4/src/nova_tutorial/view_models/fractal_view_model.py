import os
from nova.galaxy import Nova, Parameters, Tool
from nova.mvvm.interface import BindingInterface
from pydantic import BaseModel, ValidationError
from typing import Literal

from ..models.fractal import Fractal


class FractalToolInput(BaseModel):
    fractal_type: Literal["mandelbrot", "julia", "random", "markus"]


class FractalViewModel():
    def __init__(self, binding: BindingInterface):
        super().__init__()
        self.fractal = Fractal()

        self._fractal_type = "mandelbrot"
        self._run_button_disabled = True
        self._message = ""

        self.run_button_disabled_bind = binding.new_bind(
            linked_object=self,
            linked_object_arguments=["run_button_disabled"],
        )
        self.message_bind = binding.new_bind(
            linked_object=self,
            linked_object_arguments=["message"],
        )
        self.fractal_type_bind = binding.new_bind(
            linked_object=self, 
            linked_object_arguments=["fractal_type"]
        )

    def set_fractal_type(self, fractal_type: str):
        try:
            FractalToolInput(fractal_type=fractal_type)
        except ValidationError as e:
             self._message = f"Validation Error: {e}"
             self.message_bind.update_in_view(self)
             return
        self._fractal_type = fractal_type

    def run_fractal_tool(self):
        self._run_button_disabled = True
        try:
            self.fractal.set_fractal_type(self._fractal_type)
            self.fractal.run_fractal_tool()
            self._message = "Fractal tool finished successfully."
        except Exception as e:
            self._message = f"Error running fractal tool: {e}"
            raise e
        finally:
            self._run_button_disabled = False