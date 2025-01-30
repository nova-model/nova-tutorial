import os
from nova.galaxy import Nova, Parameters, Tool
from nova.mvvm.interface import BindingInterface
from pydantic import BaseModel, Field,ValidationError
from typing import Literal

from ..models.fractal import Fractal


class FractalToolInput(BaseModel):
    fractal_type: Literal["mandelbrot", "julia", "random", "markus"] = Field(default="mandelbrot")


class FractalViewModel():
    def __init__(self, binding: BindingInterface):
        super().__init__()
        self.fractal = Fractal()

        self._fractal_type = FractalToolInput()
        self._job_status:dict[str, Any] = {}
        self._message: str = ""


        self.job_status_bind = binding.new_bind(
            linked_object=self._job_status
        )
        self.message_bind = binding.new_bind(
            linked_object=self._message,
        )
        self.fractal_type_bind = binding.new_bind(
            linked_object=self._fractal_type,
        )


    def init_view(self):
        self._job_status["fractal"] = "Starting"
        self.job_status_bind.update_in_view(self._job_status)

    def set_fractal_type(self, fractal_type: str):
        try:
            FractalToolInput(fractal_type=fractal_type)
        except ValidationError as e:
             self._message = f"Validation Error: {e}"
             self.message_bind.update_in_view(self)
             return
        self._fractal_type = fractal_type
        print(f"Set new fractal type to: {self._fractal_type}")

    def run_fractal_tool(self):
        self._job_status["fractal"] = "Starting"
        self.fractal_type_bind.update_in_view(self._fractal_type)
        self.job_status_bind.update_in_view(self._job_status)
        try:
            self.fractal.set_fractal_type(self._fractal_type.fractal_type)
            self.fractal.run_fractal_tool()
            self._message = "Fractal tool finished successfully."
        except Exception as e:
            self._message = f"Error running fractal tool: {e}"
            raise e
        finally:
            self._job_status["fractal"] = ""
            self.job_status_bind.update_in_view(self._job_status)