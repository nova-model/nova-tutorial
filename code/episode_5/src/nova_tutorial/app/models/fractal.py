import os
from base64 import b64encode

from pydantic import BaseModel, Field
from nova.galaxy import Connection, Parameters, Tool


class Fractal(BaseModel):
    fractal_type_options: list[str] = ["mandelbrot", "julia", "random", "markus"]
    fractal_type: str = Field(default="mandelbrot")
    galaxy_url: str = Field(default_factory=lambda: os.getenv("GALAXY_URL"), description="NDIP Galaxy URL")
    galaxy_key: str = Field(default_factory=lambda: os.getenv("GALAXY_API_KEY"), description="NDIP Galaxy API Key")
    image_data: str = Field(default="", description="Base64 encoded PNG")

    def run_fractal_tool(self):
        conn = Connection(galaxy_url=self.galaxy_url, galaxy_key=self.galaxy_key)
        tool = Tool(id="neutrons_fractal")
        params = Parameters()
        params.add_input(name="option", value=self.fractal_type)

        with conn.connect() as galaxy_connection:
            data_store = galaxy_connection.create_data_store(name="fractal_store")
            data_store.persist()
            print("Executing fractal tool. This might take a few minutes.")
            output = tool.run(data_store, params)
            output.get_dataset("output").download("tmp.png")

            with open("tmp.png", "rb") as image_file:
                self.image_data = f"data:image/png;base64,{b64encode(image_file.read()).decode()}"
        print("Fractal tool finished successfully.")
