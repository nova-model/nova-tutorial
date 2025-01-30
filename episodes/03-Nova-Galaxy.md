---
title: "Using NDIP for Backend Computations"
teaching: 10
exercises: 3
---

# Using NDIP for Backend Computations
In this section, we will start using the `nova-galaxy` library to interact with the NDIP platform and run a neutron analysis tool.  First, ensure you have set your `GALAXY_URL` and `GALAXY_API_KEY` as environment variables, as explained in the notes at the end of this episode.  We also need to add `nova-galaxy` as a project dependency.

Open the `pyproject.toml` file in your project and add `nova-galaxy = "^0.4.0"` under `[tool.poetry.dependencies]`. Then, run `poetry install` to update your project dependencies.

## Interacting with NDIP via `nova-galaxy`

The `nova-galaxy` library is your gateway to interacting with NDIP programmatically from Python. It provides a set of classes and functions that simplify common NDIP operations, such as connecting to the platform, running tools, and managing data.

We will be using the following key classes from `nova-galaxy` in this episode:

*   **`Nova`**:  The main entry point for interacting with NDIP. You instantiate the `Nova` class with your NDIP URL and API key to establish a connection.
*   **`Tool`**: Represents a tool available on the NDIP platform. You can define a `Tool` object by its ID (which corresponds to a tool XML definition in NDIP).
*   **`Parameters`**:  Used to define the input parameters for a tool. You add parameters to a `Parameters` object, specifying the parameter names and values.

The basic workflow for running a tool with `nova-galaxy` involves these steps:

1.  **Connect to NDIP**: Create a `Nova` instance with your credentials.
2.  **Define the Tool**: Create a `Tool` instance, specifying the ID of the NDIP tool you want to run.
3.  **Set Parameters**: Create a `Parameters` instance and add the necessary input parameters and their values for the tool.
4.  **Run the Tool**: Use the `tool.run()` method to submit the job to NDIP. This typically involves creating a datastore to hold the job's input and output data.

## Creating a Model of a Tool

Let's create a `Fractal` class that uses `nova-galaxy` to run the `neutrons_fractal` tool on NDIP. You can find the complete code for this episode in the `code/episode_3` directory. Here, we will focus on the key code snippets and explain the important parts.

**1. `Fractal` Class (`src/nova_tutorial/models/fractal.py`):**

*   **Imports**:  The `Fractal Model` starts by importing necessary classes from `nova-galaxy`:

    ```python
    from nova.galaxy import Nova, Parameters, Tool
    ```

*   **`__init__` method**:  In the `__init__` method, we instantiate the `Fractal` class. Note how we retrieve `GALAXY_URL` and `GALAXY_API_KEY` from environment variables. This establishes how we will connect to NDIP:

    ```python
    class Fractal:
        def __init__(self):
            self.fractal_type = "mandelbrot"  # Default fractal type
            self.galaxy_url = os.getenv("GALAXY_URL")
            self.galaxy_key = os.getenv("GALAXY_API_KEY")
    ```

*   **`run_fractal_tool` method**: This method encapsulates the logic for running the `fractal` tool. Let's examine the key steps within this method:

    *   **Instantiate `Nova`, `Tool`, and `Parameters`**: We create instances of the `Nova`, `Tool`, and `Parameters` classes:
        ```python
            nova = Nova(galaxy_url=self.galaxy_url, galaxy_key=self.galaxy_key)
            tool = Tool(id="neutrons_fractal")
            params = Parameters()
            params.add_input(name="fractal_type", value=self.fractal_type)

        ```
        Note that we create a `Tool` object with the `id="neutrons_fractal"`. This tells `nova-galaxy` which NDIP tool we want to run. The obvious question at this point is how do we know the id of the tool and what parameters it expects? We can look at the tool's launch page in calvera for some hints but ultimately we have to look at the tool's [xml file](https://code.ornl.gov/ndip/galaxy-tools/-/blob/dev/tools/neutrons/test_tools/fractal.xml?ref_type=heads). 

    *   **Connect and Run the Tool**:  The `with nova.connect() as galaxy_connection:` block establishes a connection to NDIP and ensures proper handling of the connection:
        ```python
            with nova.connect() as galaxy_connection:
                data_store = galaxy_connection.create_data_store(name="fractal_store")
                tool.run(data_store, params)
        
        ```


**2. `main.py` - Calling the Model (`src/nova_tutorial/main.py`):**

*   **Instantiate and Run**: In the `main()` function, we create an instance of `FractalViewModel` and call the `run_fractal_tool()` method, wrapped in a `try...except` block for basic error handling:
    ```python
    def main():
        fractal = Fractal()
        try:
            fractal.run_fractal_tool()
        except Exception as e:
            print(f"Error running fractal tool: {e}")

    ```

## Running the tool

To run the code, use the following command in the top level of your `nova_tutorial` project:

```bash
poetry run app
```

You should see `Fractal tool finished successfully.` printed to the console.

## Next Steps

In this section, you learned how to use the `nova-galaxy` library to run a tool on NDIP. In the next sections, we will expand on this to create a full user interface to make this functionality accessible to the end user.

## Exercises

1.  **Run with Different Fractal Types:** Modify the `FractalViewModel` class to default to a different fractal type (e.g., "julia"). Run the application again and verify that it still works.
2.  **Introduce an Error:**  Comment out the line `params.add_input(name="fractal_type", value=self.fractal_type)` in the `run_fractal_tool` method. Run the application. What output do you see? Why do you think this error occurred? (Hint: Consider what input the `neutrons_fractal` tool expects.)
3.  **Explore `nova-galaxy` Documentation:** Open the `nova-galaxy` library source code that was provided earlier. Look at the `Nova` class and the `Tool` class. Identify at least two other methods available in these classes and briefly describe what they do based on their names and docstrings.

## References

*   **Nova Documentation**: https://nova-application-development.readthedocs.io/en/latest/
*   **nova-galaxy documentation**: https://nova-application-development.readthedocs.io/projects/nova-galaxy/en/latest/
*   **nova-trame documentation**: https://nova-application-development.readthedocs.io/projects/nova-trame/en/stable/
*   **nova-mvvm documentation**: https://nova-application-development.readthedocs.io/projects/mvvm-lib/en/latest/