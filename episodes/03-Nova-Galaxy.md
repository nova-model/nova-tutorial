---
title: "Invoking an NDIP tool"
teaching: 10
exercises: 3
---

::::::::::::::::::::::::::::::::::::::: objectives

- Explain the purpose of the `Nova`, `Tool`, and `Parameters` classes in `nova-galaxy`.
- Describe the basic workflow for running an NDIP tool using `nova-galaxy`.
- Connect to NDIP using the `Nova` class.
- Define an NDIP tool and set its parameters using the `Tool` and `Parameters` classes.
- Run the tool and create a datastore.

::::::::::::::::::::::::::::::::::::::::::::::::::

:::::::::::::::::::::::::::::::::::::::: questions

- How can I interact with the NDIP platform programmatically from Python?
- What is the `nova-galaxy` library, and how does it simplify NDIP operations?
- How do I define an NDIP tool and specify its input parameters using `nova-galaxy`?
- Where can I find information about what NDIP tool to use and parameters to set?

::::::::::::::::::::::::::::::::::::::::::::::::::

# Using NDIP for Backend Computations
In this section, we will start using the `nova-galaxy` library to interact with the NDIP platform and run a neutron analysis tool.  First, ensure you have set your `GALAXY_URL` and `GALAXY_API_KEY` as environment variables, as explained in the notes at the end of this episode.  We also need to add `nova-galaxy` as a project dependency.

From the command line, type `poetry add nova-galaxy@^0.4.0`. This command will add the nova-galaxy library to the pyproject.toml file as a project dependency. Then run `poetry install` to update your project dependencies.

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
4.  **Run the Tool**: Use the `tool.run()` method to submit the job to NDIP. This typically involves creating a datastore to hold the job\'s input and output data.

## Running the Fractal tool

Let\'s create a `Fractal` class that uses `nova-galaxy` to run the `neutrons_fractal` tool on NDIP. You can find the complete code for this episode in the `code/episode_3` directory. Here, we will focus on the key code snippets and explain the important parts.

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

*   **`run_fractal_tool` method**: This method encapsulates the logic for running the `fractal` tool. Let\'s examine the key steps within this method:

    *   **Instantiate `Nova`, `Tool`, and `Parameters`**: We create instances of the `Nova`, `Tool`, and `Parameters` classes:
        ```python
            nova = Nova(galaxy_url=self.galaxy_url, galaxy_key=self.galaxy_key)
            tool = Tool(id="neutrons_fractal")
            params = Parameters()
            params.add_input(name="fractal_type", value=self.fractal_type)

        ```
        Note that we create a `Tool` object with the `id="neutrons_fractal"`. This tells `nova-galaxy` which NDIP tool we want to run. The obvious question at this point is how do we know the id of the tool and what parameters it expects? We can look at the tool\'s launch page in calvera for some hints but ultimately we have to look at the tool\'s [xml file](https://code.ornl.gov/ndip/galaxy-tools/-/blob/dev/tools/neutrons/test_tools/fractal.xml?ref_type=heads). 

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

::::::::::::::::::::::::::::::::::::::::: callout
By default, trame will open a new tab in the browser and bring it to focus. If this is undesired behavior, it can be prevented by using ```poetry run app --server```.

::::::::::::::::::::::::::::::::::::::::::::::::::

## Asynchronous tool execution

At times, it may be desirable to execute a tool or workflow without waiting on the result. The class Tool method run has an optional `wait` parameter. The default is true so that the tool is run in a blocking manner. However, by setting the parameter to false, the tool will be run asynchronously in a non-blocking manner.

```
            output = tool.run(data_store, params, wait=False)
```

## Tool output

After the tool finishes running on NDIP, the result of the tool is returned as an output. In this example, the output is a single image file of the generated fractal. Tools can return single files or a collection of files as a zip. The output can be used by the rest of your application, saved, or simply discarded. A copy of the output also resides on the NDIP platform, so it is not necessary to maintain a local copy.

## Next Steps

In this section, you learned how to use the `nova-galaxy` library to run a tool on NDIP. In the next sections, we will expand on this to create a full user interface to make this functionality accessible to the end user.

:::::::::::::::::::::::::::::::::::::::  challenge
**Run with Different Fractal Types** 
Modify the `FractalViewModel` class to default to a different fractal type (e.g., "julia"). Run the application again and verify that it still works.

:::::::::::::::  solution
The simplest way to accomplish this is to change the default for fractal type in the Fractal class. You can easily observe the change in galaxy.
:::::::::::::::::::::::::
::::::::::::::::::::::::::::::::::::::::::::::::::

:::::::::::::::::::::::::::::::::::::::  challenge
**Introduce an Error**
Introduce an error into the code by changing the tool id to something different. What ouput do you see? What if you change the fractal_type to an invalid option such as mandel instead of mandelbrot?

:::::::::::::::  solution
In both cases, an error is received from the ndip-galaxy library. When changing the tool id, a `Tool not found` error will be returned. When selecting an invalid parameter, a `parameter 'option': an invalid option was selected` error will be returned.
:::::::::::::::::::::::::
::::::::::::::::::::::::::::::::::::::::::::::::::


## References

*   **Nova Documentation**: https://nova-application-development.readthedocs.io/en/latest/
*   **nova-galaxy documentation**: https://nova-application-development.readthedocs.io/projects/nova-galaxy/en/latest/
*   **nova-trame documentation**: https://nova-application-development.readthedocs.io/projects/nova-trame/en/stable/
*   **nova-mvvm documentation**: https://nova-application-development.readthedocs.io/projects/mvvm-lib/en/latest/