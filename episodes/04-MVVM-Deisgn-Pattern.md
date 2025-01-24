---
title: "User Interface Best Practices: The MVVM Design Pattern"
teaching: 10
exercises: 0
---

# 4. User Interface Best Practices: The MVVM Design Pattern

In this section, we will introduce the Model-View-ViewModel (MVVM) design pattern, and explore how to implement it using the `nova-mvvm` library. We will also introduce Pydantic for data validation and model definition.

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
*   **`Communicator`**: This is a class that is responsible for managing the communication between the ViewModel/Model and the View. For example, `TrameCommunicator` is a `Communicator` used in Trame.  The `Communicator` contains a `connect` method, which establishes the connection between a GUI element and a linked object and will return a callback that the UI can use to trigger model updates. It also contains an `update_in_view` method which will update the UI with new state changes.
*   **`new_bind`**: This method returns an object that contains a `connect` method, and an `update_in_view` method.
    *   The connect method establishes the connection between a GUI element and a linked object and will return a callback that the UI can use to trigger model updates.
    *    The update_in_view will update the UI with new state changes.

## Introduction to Pydantic for Data Modeling

Pydantic is a Python library that we will use to define data models and enforce data validation in our application. It uses Python type hints to define the structure of your data and automatically validates data against these types at runtime.

Benefits of Pydantic:

*   **Data Validation:** Automatically validates data types and constraints, ensuring data integrity.
*   **Clear Data Structures:**  Defines data models in a clear and readable way using Python type hints.
*   **Serialization and Deserialization:** Easily serializes data to and from standard formats like JSON.
*   **Improved Code Readability:**  Makes code easier to understand and maintain by explicitly defining data models.

## Implementing MVVM with `nova-mvvm` and Pydantic - Key Code Snippets

Let's see how to implement the MVVM pattern using `nova-mvvm` and incorporate Pydantic for data validation in our `FractalViewModel`. You can find the complete code for this episode in the `code/episode_4` directory. Here, we will focus on the key code snippets and explain the important parts.

**1. `FractalToolInput` Pydantic Model (`src/nova_tutorial/view_models/fractal_view_model.py`):**

*   **Defining the Model**: We start by defining a Pydantic model `FractalToolInput` to represent the input data for our fractal tool. This model uses type hints and `Literal` to enforce valid `fractal_type` values:

    ```python
    from pydantic import BaseModel, ValidationError
    from typing import Literal

    class FractalToolInput(BaseModel):
        fractal_type: Literal["mandelbrot", "julia", "random", "markus"]
    ```
    By defining `fractal_type` with `Literal[...]`, we ensure that only the specified string values are accepted, leveraging Pydantic's data validation capabilities.

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
            self._fractal_type = "mandelbrot"  # Default fractal type
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
            self.fractal_type_bind = binding.new_bind(linked_object=self, linked_object_arguments=["_fractal_type"])
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
    Here, `FractalToolInput(fractal_type=fractal_type)` attempts to create an instance of the Pydantic model, which triggers validation. If `fractal_type` is invalid, a `ValidationError` is caught, and the error message is set in the ViewModel's `_message` state, which, thanks to binding, *will later* update the UI.

*   **`run_fractal_tool` method**:  In `run_fractal_tool`, we now also use the `message_bind` and `run_button_disabled_bind` to update the UI state (even though we don't have a UI yet, this demonstrates good MVVM practice):

    ```python
        def run_fractal_tool(self):
            # ... (Credential check - no changes) ...

            self._run_button_disabled = True
            self.run_button_disabled_bind.update_in_view(self._run_button_disabled) # Disable button state
            try:
                # ... (nova-galaxy tool execution - no changes) ...
                self._message = "Fractal tool finished successfully."
            except Exception as e:
                self._message = f"Error running fractal tool: {e}"
            finally:
                self.message_bind.update_in_view(self._message) # Update message state
                self._run_button_disabled = False
                self.run_button_disabled_bind.update_in_view(self._run_button_disabled) # Re-enable button state
    ```
    Even without a View, we are now correctly using `update_in_view` to signal state changes for `_message` and `_run_button_disabled`, adhering to MVVM principles.

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
        binding = TrameBinding(server.state) # Instantiate TrameBinding
        fractal_vm = FractalViewModel(binding) # Pass binding to ViewModel
        # ... (rest of main function - no changes) ...
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
        *   The "Current fractal type (after attempt):" is still "mandelbrot" (or whatever the default was), indicating the invalid update was rejected.
        *   The "Current message:" now contains a "Validation Error" message from Pydantic.

2.  **Inspect ViewModel State:**
    *   In `src/nova_tutorial/view_models/fractal_view_model.py`, add `print` statements within the `FractalViewModel.__init__` method to print the initial values of `self._fractal_type`, `self._run_button_disabled`, and `self._message`.
    *   Run the application (`poetry run app`). Observe the output in the console. Verify that the initial values are printed as expected ("mandelbrot", `False`, and "").
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
        *   *(Optional): You could add print statements in the `fractal_type.setter` to further observe the update process.*