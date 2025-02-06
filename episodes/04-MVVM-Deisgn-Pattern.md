---
title: "User Interface Best Practices: The MVVM Design Pattern"
teaching: 10
exercises: 0
---

# 4. User Interface Best Practices: The MVVM Design Pattern

In this section, we will introduce the Model-View-ViewModel (MVVM) design pattern, a powerful architectural approach for structuring applications, particularly those with user interfaces. We\'ll explore the core principles of MVVM, the roles of each component, and how the NOVA framework simplifies its implementation, making your code more organized, testable, and maintainable.

## What is a Design Pattern?

Before diving into MVVM, it\'s helpful to understand what a *design pattern* is in software development. A design pattern is a reusable solution to a commonly occurring problem in software design. It\'s not a code snippet you can copy and paste, but rather a template or blueprint for how to structure your code to achieve a specific goal (e.g., separation of concerns, code reusability, testability).

## The Model-View-ViewModel (MVVM) Pattern

MVVM is an architectural design pattern specifically designed for applications with user interfaces (UIs). It aims to separate the UI (the View) from the underlying data and logic (the Model) by introducing an intermediary component called the ViewModel. This separation makes the application more maintainable, testable, and easier to evolve.

The MVVM pattern consists of three core components:

*   **Model:** The Model represents the *data* and the *business logic* of the application. It\'s responsible for:
    *   Data storage (e.g., reading from and writing to a database, a file, or an API).
    *   Data validation (ensuring the data is in a valid state).
    *   Business rules (the logic that governs how the data is manipulated and used).

    The Model is *agnostic* to the UI. It doesn\'t know anything about how the data will be displayed or how the user will interact with it. It simply provides the data and the means to manipulate it.

    *In the context of our NOVA tutorial, the Model will often include the logic for interacting with the NDIP platform via `nova-galaxy`.*

*   **View:** The View is the *user interface* (UI) of the application. It\'s responsible for:
    *   Displaying data to the user.
    *   Capturing user input (e.g., button clicks, text entered in a field, selections from a dropdown).
    *   Presenting the application\'s visual appearance.

    The View is *passive*. It doesn\'t contain any business logic or data manipulation code. It simply displays the data provided to it and relays user actions to the ViewModel.

    *In our NOVA tutorial, the View will be built using Trame and Vuetify components, leveraging the styling and structure provided by `nova-trame`.*

*   **ViewModel:** The ViewModel acts as an *intermediary* between the Model and the View. It\'s responsible for:
    *   Preparing data from the Model for display in the View. This might involve formatting the data, combining data from multiple sources, or creating derived data.
    *   Handling user actions from the View. This might involve validating user input, updating the Model, or triggering other actions in the application.
    *   Exposing data and commands to the View through *data binding*.

    The ViewModel is *UI-specific*. It knows about the View and the data that the View needs, but it doesn\'t know about the specific UI elements that are used to display the data. It also orchestrates the interaction between the View and the Model.

    *The ViewModel is where we\'ll use `nova-mvvm` to create bindings between the ViewModel and the View, enabling the reactive updates.*

## Why Use MVVM? (Benefits)

The MVVM pattern provides several benefits:

*   **Separation of Concerns:** MVVM clearly separates the UI (View) from the application logic (Model) and the presentation logic (ViewModel). This makes the code more organized and easier to understand.
*   **Testability:** Because the ViewModel is independent of the View, it can be easily unit-tested. You can test the presentation logic without needing to create a UI.
*   **Maintainability:** Changes to the UI are less likely to affect the underlying application logic, and vice versa. This makes the application easier to maintain and evolve over time.
*   **Reusability:** The ViewModel can be reused with different Views, allowing you to create different UIs for the same underlying data and logic.
*   **Team Collaboration:** MVVM facilitates collaboration between developers and UI designers. Developers can focus on the Model and ViewModel, while designers can focus on the View, without interfering with each other\'s work.

## Data Binding: The Heart of MVVM

*Data binding* is a mechanism that allows the View and the ViewModel to automatically synchronize their data. When the data in the ViewModel changes, the View is automatically updated to reflect the changes. Conversely, when the user interacts with the View (e.g., by entering text in a field), the data in the ViewModel is automatically updated.

This data binding is what makes MVVM so powerful and allows for reactive UIs. Instead of manually writing code to update the UI every time the data changes, you simply bind the UI elements to the data in the ViewModel, and the updates happen automatically.

## How NOVA Simplifies MVVM

The NOVA framework provides libraries and tools that simplify the implementation of the MVVM pattern:

*   **`nova-mvvm`**: This library provides a set of classes and functions that make it easier to create bindings between the ViewModel and the View. It handles the low-level details of data synchronization, allowing you to focus on the application logic.
*   **`nova-trame`**: Provides a set of pre-built components and layouts that are designed to work seamlessly with `nova-mvvm`. This simplifies the creation of the View and ensures a consistent look and feel across NOVA applications.
*   **Pydantic:** While not strictly part of the MVVM pattern, Pydantic helps define the structure of your Model and ViewModel, making it easier to validate data and ensure data integrity.

## Introduction to Pydantic for Data Modeling

Pydantic is a Python library that we will use to define data models and enforce data validation in our application. It uses Python type hints to define the structure of your data and automatically validates data against these types at runtime.

Benefits of Pydantic:

*   **Data Validation:** Automatically validates data types and constraints, ensuring data integrity.
*   **Clear Data Structures:**  Defines data models in a clear and readable way using Python type hints.
*   **Serialization and Deserialization:** Easily serializes data to and from standard formats like JSON.
*   **Improved Code Readability:**  Makes code easier to understand and maintain by explicitly defining data models.

## Implementing MVVM with `nova-mvvm` and Pydantic - Key Code Snippets

Let\'s see how to implement the MVVM pattern using `nova-mvvm` and incorporate Pydantic for data validation in our `FractalViewModel`. You can find the complete code for this episode in the `code/episode_4` directory. Here, we will focus on the key code snippets and explain the important parts.

**1. `FractalToolInput` Pydantic Model (`src/nova_tutorial/view_models/fractal_view_model.py`):**

*   **Defining the Model**: We start by defining a Pydantic model `FractalToolInput` to represent the input data for our fractal tool. This model uses type hints and `Literal` to enforce valid `fractal_type` values:

    ```python
    from pydantic import BaseModel, ValidationError
    from typing import Literal

    class FractalToolInput(BaseModel):
        fractal_type: Literal["mandelbrot", "julia", "random", "markus"]
    ```
    By defining `fractal_type` with `Literal[...]`, we ensure that only the specified string values are accepted, leveraging Pydantic\'s data validation capabilities.

**2. `FractalViewModel` Class (`src/nova_tutorial/view_models/fractal_view_model.py`):**

*   **Imports**:  The `FractalViewModel` now imports classes from `nova.mvvm.interface` and `nova.mvvm.trame_binding`, and `pydantic`:

    ```python
    from nova.mvvm.interface import BindingInterface
    from nova.mvvm.trame_binding import TrameBinding
    ```

*   **`__init__` method**:  In the `__init__` method, we now accept a `BindingInterface` instance (specifically, `TrameBinding`) as an argument. We also initialize state variables with leading underscores ( `_fractal_type`, `_run_button_disabled`, `_message`) to follow a convention for "internal" variables, and create bindings using `binding.new_bind(...)`:

    ```python
    class FractalViewModel():
    def __init__(self, binding: BindingInterface):
        super().__init__()
        self.fractal = Fractal()

        self._fractal_type = "mandelbrot"
        self._run_button_disabled = True
        self._message = ""

        self.run_button_disabled_bind = binding.new_bind(
            linked_object=self,
            linked_object_arguments=["run_button_disabled"],
        )
        self.message_bind = binding.new_bind(
            linked_object=self,
            linked_object_arguments=["message"],
        )
        self.fractal_type_bind = binding.new_bind(
            linked_object=self, 
            linked_object_arguments=["fractal_type"]
        )
    ```
    The `binding.new_bind(...)` calls are crucial for setting up the MVVM pattern. They create `Communicator` objects that will manage the synchronization of state between the ViewModel and the View (UI).

*   **`set_fractal_type` method**: We modify `set_fractal_type` to use the `FractalToolInput` Pydantic model for validation. If validation fails, we update the `_message` state variable with the error:

    ```python
        def set_fractal_type(self, fractal_type: str):
            try:
                FractalToolInput(fractal_type=fractal_type) # Validate input using Pydantic
            except ValidationError as e:
                self._message = f"Validation Error: {e}"
                self.message_bind.update_in_view(self._message) # Update message state
                return
            self._fractal_type = fractal_type
            self.fractal_type_bind.update_in_view(self._fractal_type) # Update fractal_type state
    ```
    Here, `FractalToolInput(fractal_type=fractal_type)` attempts to create an instance of the Pydantic model, which triggers validation. If `fractal_type` is invalid, a `ValidationError` is caught, and the error message is set in the ViewModel\'s `_message` state, which, thanks to binding, *will later* update the UI.

*   **`run_fractal_tool` method**:  In `run_fractal_tool`, we now also use the `message_bind` and `run_button_disabled_bind` to update the UI state (even though we don\'t have a UI yet, this demonstrates good MVVM practice):

    ```python
    def run_fractal_tool(self):
        self._job_status["fractal"] = "Starting"
        try:
            self.fractal.set_fractal_type(self._fractal_type.fractal_type)
            self.fractal.run_fractal_tool()
            self._message = "Fractal tool finished successfully."
        except Exception as e:
            self._message = f"Error running fractal tool: {e}"
            raise e
        self._job_status["fractal"] = "Completed"
    ```
    Even without a View, we are already considering what the functionality that we\'ll need to support. We\'ve already created the bindings to server as our communicators between our future view and our new view model.

**2. `main.py` - Wiring up TrameBinding (`src/nova_tutorial/main.py`):**

*   **Import `TrameBinding`**: We import `TrameBinding` from `nova.mvvm.trame_binding`:
    ```python
    # src/nova_tutorial/main.py
    from nova.mvvm.trame_binding import TrameBinding
    ```

*   **Instantiate `TrameBinding` and Pass to ViewModel**: In `main()`, we now create a `TrameBinding` instance and pass it to the `FractalViewModel` constructor:

    ```python
    def main():
        server = get_server(None, client_type="vue3") # Trame server (not yet used for UI in this episode)
        binding = TrameBinding(server.state)
        fractal_vm = FractalViewModel(binding)
    ```
    This is the crucial step that "wires up" the ViewModel to the Trame binding, making it ready to interact with a Trame-based View in later episodes.


## Running the application

To run the code, use the following command in the top level of your `nova_tutorial` project:

```bash
poetry run app
```

You should see `Fractal tool finished successfully.` printed to the console, although we have not created a UI yet.

## Exercises

1.  **Trigger Pydantic Validation Error (Programmatic):**
    *   In `FractalViewModel` in `src/nova_tutorial/view_models/fractal_view_model.py`, modify the `update_fractal_programmatically` function from the previous exercise to use an *invalid* fractal type:
        ```python
        def update_fractal_programmatically(new_type: str):
            self.fractal_type = new_type # Use the setter which includes validation
            print("Attempted to set fractal type programmatically to:", new_type)
            print("Current fractal type (after attempt):", self._fractal_type) # Print value after attempt
            print("Current message:", self._message) # Print message

        update_fractal_programmatically("invalid-fractal-type") # Programmatically update to invalid type
        ```
    *   Run the application (`poetry run app`). Observe the console output. Verify that:
        *   The message "Attempted to set fractal type programmatically to: invalid-fractal-type" is printed.
        *   The "Current fractal type (after attempt):" is still "mandelbrot" indicating the invalid update was rejected.
        *   The "Current message:" now contains a "Validation Error" message from Pydantic.

2.  **Inspect ViewModel State:**
    *   In `src/nova_tutorial/view_models/fractal_view_model.py`, add `print` statements within the `FractalViewModel.__init__` method to print the initial values of `self._fractal_type`, `self._job_status`, and `self._message`.
    *   Run the application (`poetry run app`). Observe the output in the console. Verify that the initial values are printed as expected.
    *   Now, modify the `FractalViewModel.__init__` method to change the initial value of `self._message` to "Application starting...". Run the application again and confirm that the printed initial message has changed.

3.  **Programmatic State Update and Binding:**
    *   In `FractalViewModel` in `src/nova_tutorial/view_models/fractal_view_model.py`, after the line `self.fractal_type_bind = binding.new_bind(...)` in `__init__`, add the following lines:
        ```python
        print("Initial fractal type:", self._fractal_type) # Print initial value

        def update_fractal_programmatically(new_type: str):
            self.fractal_type = new_type # Use the setter to trigger validation and updates
            print("Fractal type updated programmatically to:", self._fractal_type)

        update_fractal_programmatically("julia") # Programmatically update fractal_type
        print("Fractal type after programmatic update:", self._fractal_type)
        ```
    *   Run the application (`poetry run app`). Observe the console output. Verify that:
        *   The initial fractal type is printed as "mandelbrot".
        *   The message "Fractal type updated programmatically to: julia" is printed.
        *   The final fractal type (after programmatic update) is printed as "julia".

## References

*   **Nova Documentation**: https://nova-application-development.readthedocs.io/en/latest/
*   **nova-galaxy documentation**: https://nova-application-development.readthedocs.io/projects/nova-galaxy/en/latest/
*   **nova-trame documentation**: https://nova-application-development.readthedocs.io/projects/nova-trame/en/stable/
*   **nova-mvvm documentation**: https://nova-application-development.readthedocs.io/projects/mvvm-lib/en/latest/