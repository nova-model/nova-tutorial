```markdown
# MVVM Design Pattern with `nova-mvvm`

In this section, we will delve deeper into the Model-View-ViewModel (MVVM) design pattern and explore how to implement it using the `nova-mvvm` library.

## Introduction to MVVM

The Model-View-ViewModel (MVVM) pattern is an architectural pattern used to structure applications, particularly those with user interfaces. It promotes a separation of concerns, making code more organized, testable, and maintainable.

*   **Model:** The Model represents the application's data and business logic. It is responsible for retrieving, managing, and modifying data. It is not directly concerned with how the data is displayed.
*   **View:** The View is the user interface (UI) that the user interacts with. It displays data to the user and captures user interactions. In this section, we will not be using a UI but when we do, this will be where UI components will be placed.
*   **ViewModel:** The ViewModel acts as an intermediary between the Model and the View. It exposes the data from the Model in a way that is easy for the View to display. It also handles user interactions, and updates the Model accordingly.

The benefits of using the MVVM pattern include:

*   **Testability:** ViewModels can be unit tested independently of the View, which allows for more complete and thorough testing.
*   **Maintainability:** The clear separation of concerns makes it easier to maintain and refactor code. Changes to the Model are less likely to cause breaking changes in the View or ViewModel.
*   **Code Reusability:** The View and the ViewModel can be reused in different parts of the application. For example, different Views can be implemented without modifying the underlying ViewModel.
*   **Flexibility:** Provides a flexible and scalable architecture that can be adapted to different application requirements.

There are other patterns that can be used to build UIs such as MVC or MVP. We will not explore these in this tutorial, but it is important to know that other options exist.

## Core Concepts of `nova-mvvm`

The `nova-mvvm` library provides a set of tools that make it easier to implement the MVVM pattern. Here are the key concepts:

*   **`BindingInterface`**: This is an abstract class that defines the interface for creating bindings between a ViewModel/Model variable and a framework specific element. It provides the `new_bind` method, which returns a `Communicator` object.
*   **`TrameBinding`**: This is an implementation of the `BindingInterface` specifically for use with Trame. It creates `TrameCommunicator` objects.
*   **`Communicator`**: This is a class that is responsible for managing the communication between the ViewModel/Model and the View. For example, `TrameCommunicator` is a `Communicator` used in Trame.
*   **`new_bind`**: This method returns an object that contains a `connect` method, and an `update_in_view` method.
    *   The connect method establishes the connection between a GUI element and a linked object and will return a callback that the UI can use to trigger model updates.
    *    The update_in_view will update the UI with new state changes.

## Modifying Our ViewModel

Let's modify our `src/nova_tutorial/view_models/fractal_view_model.py` file to make use of `nova-mvvm`:

```python
# src/nova_tutorial/view_models/fractal_view_model.py
import os
from nova.galaxy import Nova, Parameters, Tool
from nova.mvvm.interface import BindingInterface

class FractalViewModel():
    def __init__(self, binding: BindingInterface):
        super().__init__()
        self.fractal_type = "mandelbrot"  # Default fractal type
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
        self.fractal_type_bind = binding.new_bind(linked_object=self, linked_object_arguments=["fractal_type"])


    def set_fractal_type(self, fractal_type: str):
        self.fractal_type = fractal_type
        self.fractal_type_bind.update_in_view(self.fractal_type)

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
            params.add_input(name="fractal_type", value=self.fractal_type)
            
            with nova.connect() as galaxy_connection:
                data_store = galaxy_connection.create_data_store(name="fractal_store")
                tool.run(data_store, params)
                # Datastore is deleted after function exists
            self._message = "Fractal tool finished successfully."
        except Exception as e:
            self._message = f"Error running fractal tool: {e}"
        finally:
            self._run_button_disabled = False
            self.message_bind.update_in_view(self._message)
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
```

Key Changes:

*   **BindingInterface:**  The constructor now takes in a `BindingInterface`, and utilizes it to create bindings for `run_button_disabled`, `message`, and `fractal_type`.
*   **Naming convention:** The state variables are updated to have a leading `_` which follows a common convention for private variables.
*   **`update_in_view` Calls**: All state changes are now accompanied with calls to `update_in_view`.

Finally, to run this application, let's update our `src/nova_tutorial/main.py` file to include a `TrameBinding`:

```python
# src/nova_tutorial/main.py
from nova.mvvm.trame_binding import TrameBinding
from nova_tutorial.view_models.fractal_view_model import FractalViewModel
from trame.app import get_server

def main():
    server = get_server(None, client_type="vue3")
    binding = TrameBinding(server.state)
    fractal_vm = FractalViewModel(binding)
    try:
        fractal_vm.run_fractal_tool()
    except Exception as e:
        print(f"Error running fractal tool: {e}")


if __name__ == "__main__":
    main()
```

Key changes:

*  The code now imports the trame binding and instantiates a binding.
*  The view model instance now takes in this binding.

## Running the application

To run the code, use the following command in the top level of your `nova_tutorial` project:

```bash
poetry install
poetry run app
```

You should see `Fractal tool finished successfully.` printed to the console, although we have not created a UI yet.