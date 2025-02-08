---
title: "Invoking an NDIP tool"
teaching: 10
exercises: 3
---

::::::::::::::::::::::::::::::::::::::: objectives

- Explain the purpose of the `Connection`, `Outputs`, `Datastore`, `Tool`, and `Parameters` classes in `nova-galaxy`.
- Describe the basic workflow for running an NDIP tool using `nova-galaxy`.
- Connect to NDIP using the `Connection` class.
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

From the command line, type `poetry add nova-galaxy@^0.7.0`. This command will add the nova-galaxy library to the pyproject.toml file as a project dependency. Then run `poetry install` to update your project dependencies.

## Interacting with NDIP via `nova-galaxy`

The `nova-galaxy` library is your gateway to interacting with NDIP programmatically from Python. It provides a set of classes and functions that simplify common NDIP operations, such as connecting to the platform, running tools, and managing data.

We will be using the following key classes from `nova-galaxy` in this episode:

*   **`Connection`**:  The main entry point for interacting with NDIP. You instantiate the `Connection` class with your NDIP URL and API key to establish a connection.
*   **`Tool`**: Represents a tool available on the NDIP platform. You can define a `Tool` object by its ID (which corresponds to a tool XML definition in NDIP).
*   **`Parameters`**:  Used to define the input parameters for a tool. You add parameters to a `Parameters` object, specifying the parameter names and values.
*   **`Datastore`**: Configures Galaxy to group outputs of a tool to group outputs of a tool together.
*   **`Output`**: Contains the output datasets and collections for a tool.
*   **`Dataset`**: A singular file which can be uploaded to Galaxy to be used in tools or downloaded from Galaxy to local storage.
*   **`DatasetCollection`**: A group of files which can be uploaded to Galaxy to be used in tools or downloaded from Galaxy to local storage.

The basic workflow for running a tool with `nova-galaxy` involves these steps:

1.  **Connect to NDIP**: Create a `Connection` instance with your credentials.
2.  **Define the Tool**: Create a `Tool` instance, specifying the ID of the NDIP tool you want to run.
3.  **Set Parameters**: Create a `Parameters` instance and add the necessary input parameters and their values for the tool.
4.  **Run the Tool**: Use the `tool.run()` method to submit the job to NDIP. This typically involves creating a datastore to hold the job\'s input and output data.

## Setting up the Fractal tool

Let\'s create a `Fractal` class that uses `nova-galaxy` to run the `neutrons_fractal` tool on NDIP. You can find the complete code for this episode in the `code/episode_3` directory. 

**1. `Fractal` Class (`src/nova_tutorial/app/models/fractal.py`):**

To get started, let\'s create the Fractal class. Create an empty file at `src/nova_tutorial/app/models/fractal.py`. Add the following pieces of code to the newly created file. 

*   **Imports**:  The `Fractal Class` will start by importing the necessary classes from `nova-galaxy`:

    ```python
    import os
    from nova.galaxy import Connection, Parameters, Tool
    ```

*   **`__init__` method**:  In the `__init__` method, we initialize the `Fractal` class. Note how we retrieve `GALAXY_URL` and `GALAXY_API_KEY` from environment variables. This establishes how we will connect to NDIP:

    ```python
    class Fractal:
        def __init__(self):
            self.fractal_type = "mandelbrot"  # Default fractal type
            self.galaxy_url = os.getenv("GALAXY_URL")
            self.galaxy_key = os.getenv("GALAXY_API_KEY")
    ```

*   **`run_fractal_tool` method**: This method encapsulates the logic for running the `fractal` tool. Let\'s examine the key steps within this method:

    *   **Instantiate `Connection`, `Tool`, and `Parameters`**: We create instances of the `Connection`, `Tool`, and `Parameters` classes:
        ```python
        def run_fractal_tool(self):
            conn = Connection(galaxy_url=self.galaxy_url, galaxy_key=self.galaxy_key)
            tool = Tool(id="neutrons_fractal")
            params = Parameters()
            params.add_input(name="option", value=self.fractal_type)

        ```
        Note that we create a `Tool` object with the `id="neutrons_fractal"`. This tells `nova-galaxy` which NDIP tool we want to run. The obvious question at this point is how do we know the id of the tool and what parameters it expects? We can look at the tool\'s launch page in calvera for some hints but ultimately we have to look at the tool\'s [xml file](https://code.ornl.gov/ndip/galaxy-tools/-/blob/dev/tools/neutrons/test_tools/fractal.xml?ref_type=heads). 

    *   **Connect and Run the Tool**:  The `with conn.connect() as galaxy_connection:` block establishes a connection to NDIP and ensures proper handling of the connection:

        ```python
            with conn.connect() as galaxy_connection:
                data_store = galaxy_connection.create_data_store(name="fractal_store")
                data_store.persist()
                print("Executing fractal tool. This might take a few minutes.")
                output = tool.run(data_store, params)
                output.get_dataset("output").download("tmp.png")
            print("Fractal tool finished successfully.")
        ```


**2. `main.py` - Calling the Model (`src/nova_tutorial/app/main.py`):**

We are now going to modify the existing `main.py` file. Change the main method to match the code below.

*   **Instantiate and Run**: In the `main()` function, we create an instance of `Fractal` and call the `run_fractal_tool()` method, wrapped in a `try...except` block for basic error handling:
    ```python
    import sys
    from .models.fractal import Fractal

    def main() -> None:
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

Tool execution often results in some type of output. In the Fractal example, the tool output is a singular image file. A tool can have multiple outputs and sometimes these outputs are grouped together in a collection. In `nova-galaxy`, a singular file is called a Dataset and a group of files is called a DatasetCollection. The `Dataset` and `DatasetCollection` classes support the following methods:

*   **upload(Datastore):** Uploads the Dataset(DatasetCollection) to the specified Datastore on Galaxy.
*   **download(file_path):** Downloads the Dataset(DatasetCollection) from Galaxy to the local path.
*   **get_content():** Retreives the content of the Dataset(DatasetCollection) without saving it to a local file path.

If a tool run results in a `Dataset` or `DatasetCollection`, an `Output` is returned from the run method. `Output` is an encapsulation of the output datasets and collections from a Tool. A tool execution can result in multiple `Dataset` and `DatasetCollection`, therefore, these are all grouped in the `Outputs` class for easier consumption.

In the Fractal example, the Tool.run comman returns an instance of the `Output` class which we save to the variable `output`. The Fractal tool [xml file](https://code.ornl.gov/ndip/galaxy-tools/-/blob/dev/tools/neutrons/test_tools/fractal.xml?ref_type=heads) defines that successful execution of the tool will result in a `Dataset` named `output`. This `Dataset` is then downloaded to the local file path `image.png`.

```python
    output = tool.run(data_store, params)
    output.get_dataset("output").download("image.png")
```

The Outputs can be used by the rest of your application, saved, or simply discarded. A copy of the Datasets and DatasetCollections also resides on the NDIP platform, so it is not necessary to maintain a local copy.

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

:::::::::::::::::::::::::::::::::::::::: keypoints
- Tools are run remotely on the NDIP platform
- Nova-Galaxy is used to connect to NDIP and run tools
- The fractal tool is started remotely and run on NDIP.
::::::::::::::::::::::::::::::::::::::::::::::::::