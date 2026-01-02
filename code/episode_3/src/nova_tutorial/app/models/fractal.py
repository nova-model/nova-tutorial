import os
from nova.galaxy import Connection, Parameters, Tool


class Fractal:
    def __init__(self):
        self.fractal_type = "mandelbrot"  # Default fractal type
        self.galaxy_url = os.getenv("GALAXY_URL")
        self.galaxy_key = os.getenv("GALAXY_API_KEY")

    def run_fractal_tool(self):
        conn = Connection(galaxy_url=self.galaxy_url, galaxy_key=self.galaxy_key)
        tool = Tool(id="neutrons_fractal")
        params = Parameters()
        params.add_input(name="option", value=self.fractal_type)

        with conn.connect() as galaxy_connection:
            data_store = galaxy_connection.create_data_store(name="fractal_store")
            data_store.persist()
            print("Executing fractal tool. This might take a few minutes.")
            output = tool.run(data_store, params, wait=True)
            output.get_dataset("output").download("image.png")
        print("Fractal tool finished successfully.")
