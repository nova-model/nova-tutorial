import os
from nova.galaxy import Nova, Parameters, Tool
from nova.mvvm.interface import BindingInterface
from pydantic import BaseModel, ValidationError
from typing import Literal

class FractalToolInput(BaseModel):
    fractal_type: Literal["mandelbrot", "julia", "random", "markus"]

class FractalViewModel():
    def __init__(self, binding: BindingInterface):
        super().__init__()
        self._fractal_type = "mandelbrot"  # Default fractal type
        self.galaxy_url = os.getenv("GALAXY_URL")
        self.galaxy_key = os.getenv("GALAXY_API_KEY")
        self._run_button_disabled = False
        self._message = ""
        self.run_button_disabled_bind = binding.new_bind(
            linked_object=self,
            linked_object_arguments=["_run_button_disabled"],
        )
        self.message_bind = binding.new_bind(
            linked_object=self,
            linked_object_arguments=["_message"],
        )
        self.fractal_type_bind = binding.new_bind(linked_object=self, linked_object_arguments=["_fractal_type"])


    def set_fractal_type(self, fractal_type: str):
        try:
            FractalToolInput(fractal_type=fractal_type)
        except ValidationError as e:
             self._message = f"Validation Error: {e}"
             self.message_bind.update_in_view(self._message)
             return
        self._fractal_type = fractal_type
        self.fractal_type_bind.update_in_view(self._fractal_type)

    def run_fractal_tool(self):
        """Runs the fractal tool with the current fractal type."""
        if not self.galaxy_url or not self.galaxy_key:
            self._message = "You must specify GALAXY_URL and GALAXY_API_KEY as environment variables."
            self.message_bind.update_in_view(self._message)
            return

        self._run_button_disabled = True
        self.run_button_disabled_bind.update_in_view(self._run_button_disabled)
        try:
            nova = Nova(galaxy_url=self.galaxy_url, galaxy_key=self.galaxy_key)
            tool = Tool(id="neutrons_fractal")
            params = Parameters()
            params.add_input(name="fractal_type", value=self._fractal_type)

            with nova.connect() as galaxy_connection:
                data_store = galaxy_connection.create_data_store(name="fractal_store")
                tool.run(data_store, params)
                # Datastore is deleted after function exists
            self._message = "Fractal tool finished successfully."
        except Exception as e:
            self._message = f"Error running fractal tool: {e}"
        finally:
            self.message_bind.update_in_view(self._message)
            self._run_button_disabled = False
            self.run_button_disabled_bind.update_in_view(self._run_button_disabled)

    @property
    def run_button_disabled(self):
        return self._run_button_disabled

    @run_button_disabled.setter
    def run_button_disabled(self, value):
        self._run_button_disabled = value

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, value):
        self._message = value