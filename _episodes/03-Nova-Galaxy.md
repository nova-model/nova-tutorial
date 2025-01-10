# Working with `nova-galaxy`

In this section, you will learn how to use the `nova-galaxy` library to interact with NDIP and run a neutron analysis tool. We will be using a tool with the id `neutrons_fractal` as an example.

## Setting up your environment

Before running your tool, we must first add our `GALAXY_URL` and `GALAXY_API_KEY` as environment variables. If you don't know how to do this, check the notes below this section. GALAXY_URL should be set to calvera.ornl.gov. If you don't already have an API Key, you can retrieve one by logging into calvera, navigating to users->preferences->Manage API Key. We also must add `nova-galaxy` as a dependency to our `pyproject.toml` file and then install our dependencies using poetry. 

Open the file named `pyproject.toml` and add the following under `[tool.poetry.dependencies]`

```
nova-galaxy = "^0.4.0"
```

Save this file and then run `poetry install` to install your dependencies. Once that is done, we can begin creating our view model.

## Creating a ViewModel

To begin using the `nova-galaxy` library, we will first create a class to handle the logic for submitting our jobs. Create a folder named `view_models` in your `src/nova_tutorial/` folder. Inside, create a file named `fractal_view_model.py` with the following content:

```python
# src/nova_tutorial/view_models/fractal_view_model.py
import os
from nova.galaxy import Nova, Parameters, Tool


class FractalViewModel:
    def __init__(self):
        self.fractal_type = "mandelbrot"  # Default fractal type
        self.galaxy_url = os.getenv("GALAXY_URL")
        self.galaxy_key = os.getenv("GALAXY_API_KEY")

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
        params.add_input(name="fractal_type", value=self.fractal_type)
        
        with nova.connect() as galaxy_connection:
            data_store = galaxy_connection.create_data_store(name="nova_tutorial")
            tool.run(data_store, params)
            # Datastore is deleted after function exists

        print("Fractal tool finished successfully.")
```

This code imports the `Nova`, `Parameters`, and `Tool` classes from the `nova-galaxy` library. It then defines the `FractalViewModel` class, which will be responsible for submitting our job. Let's now add some code to `src/nova_tutorial/main.py` to actually call this method:

```python
# src/nova_tutorial/main.py
from nova_tutorial.view_models.fractal_view_model import FractalViewModel

def main():
    fractal_vm = FractalViewModel()
    try:
        fractal_vm.run_fractal_tool()
    except Exception as e:
        print(f"Error running fractal tool: {e}")

if __name__ == "__main__":
    main()
```

This code instantiates a view model and then attempts to run the `run_fractal_tool` method.

## Running the tool

To run the code, use the following command in the top level of your `nova_tutorial` project:

```bash
poetry install
poetry run app
```

The application will take a few minutes to finish but when it's completed you should see `Fractal tool finished successfully.` printed to the console. You can also view the job in your history on calvera.ornl.gov.

## Next Steps

In this section, you learned how to use the `nova-galaxy` library to run a tool on NDIP. In the next sections, we will expand on this to create a full user interface to make this functionality accessible to the end user.

## Notes: Setting Environment Variables
* On linux you can set environment variables using `export GALAXY_URL=<your_url>` and `export GALAXY_API_KEY=<your_api_key>`.
* On windows, you can use `set GALAXY_URL=<your_url>` and `set GALAXY_API_KEY=<your_api_key>`.
* If you do not want to set the environment variables in your current shell, you can also modify the `FractalViewModel.__init__` method to accept the API key and url.