import os
from base64 import b64encode
from enum import Enum
from typing import Callable, Literal

from pydantic import BaseModel, Field
from nova.galaxy import Connection, Parameters, Tool


class FractalTypeOptions(str, Enum):
    mandelbrot = "mandelbrot"
    julia = "julia"
    random = "random"
    markus = "markus"


class FractalData(BaseModel):
    fractal_type: FractalTypeOptions = Field(
        default=FractalTypeOptions.mandelbrot, title="Fractal Type"
    )
    galaxy_url: str = Field(
        default=os.getenv("GALAXY_URL", ""), description="NDIP Galaxy URL"
    )
    galaxy_key: str = Field(
        default=os.getenv("GALAXY_API_KEY", ""), description="NDIP Galaxy API Key"
    )
    image_data: str = Field(default="", description="Base64 encoded PNG")


class Fractal:
    def __init__(self):
        self.data = FractalData(fractal_type="mandelbrot")

    def set_fractal_type(self, fractal_type: str):
        self.data.fractal_type = fractal_type

    def run_fractal_tool(self, progress: Callable):
        conn = Connection(
            galaxy_url=self.data.galaxy_url, galaxy_key=self.data.galaxy_key
        )
        tool = Tool(id="neutrons_fractal")
        params = Parameters()
        params.add_input(name="option", value=self.data.fractal_type)

        with conn.connect() as galaxy_connection:
            data_store = galaxy_connection.create_data_store(name="fractal_store")
            data_store.persist()
            print("Executing fractal tool. This might take a few minutes.")
            output = tool.run(data_store, params, wait=True)
            output.get_dataset("output").download("image.png")

            with open("image.png", "rb") as image_file:
                self.data.image_data = (
                    f"data:image/png;base64,{b64encode(image_file.read()).decode()}"
                )
        print("Fractal tool finished successfully.")
