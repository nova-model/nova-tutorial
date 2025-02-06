import os
import base64
from typing import Literal

from pydantic import BaseModel, Field
from nova.galaxy import Nova, Parameters, Tool


class Fractal(BaseModel):
    fractal_type: Literal["mandelbrot", "julia", "random", "markus"] = Field(default="mandelbrot")
    galaxy_url: str = Field(default_factory=lambda: os.getenv("GALAXY_URL"), description="NDIP Galaxy URL")
    galaxy_key: str = Field(default_factory=lambda: os.getenv("GALAXY_API_KEY"), description="NDIP Galaxy API Key")
    image_data: str = Field(default="", description="Base64 encoded PNG")

    def set_fractal_type(self, fractal_type: str):
        self.fractal_type = fractal_type

    def run_fractal_tool(self):
        """Runs the fractal tool with the current fractal type."""
        if not self.galaxy_url or not self.galaxy_key:
            raise Exception(
                "You must specify GALAXY_URL and GALAXY_API_KEY as environment variables."
            )

        nova = Nova(galaxy_url=self.galaxy_url, galaxy_key=self.galaxy_key)
        tool = Tool(id="neutrons_fractal")
        params = Parameters()

        with nova.connect() as galaxy_connection:
            data_store = galaxy_connection.create_data_store(name="fractal_store")
            data_store.persist()
            output = tool.run(data_store, params)
            output.get_dataset("output").download("tmp.png")

        print("Fractal tool finished successfully.")
