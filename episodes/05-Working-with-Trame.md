---
title: "Web-based User Interface Development"
teaching: 10
exercises: 3
---
# Web-based User Interface Development

In this section, we will introduce Trame and the `nova-trame` library to start building a web-based user interface for our NOVA application. We'll cover the benefits of Trame and how `nova-trame` simplifies UI development within the NOVA ecosystem.

## Introduction to Trame

Trame is a powerful Python framework for building interactive web-based user interfaces and visualizations, all without needing to write Javascript or complex web code directly. It allows you to describe your UI declaratively using Python, and Trame handles the complexities of creating a dynamic web application.

Key Features and Benefits of Trame:

*   **Declarative UI:** Describe your user interfaces using Python code, focusing on *what* the UI should be, not *how* to implement it in web technologies.
*   **Interactive Applications:** Create dynamic UIs with real-time updates through Trame's data binding. Changes in your ViewModel automatically reflect in the UI, and user interactions in the UI can update the ViewModel.
*   **Web-Based and Accessible:** Trame applications are standard web applications, accessible from any modern web browser, making them easy to deploy and share.
*   **Extensible and Rich UI Components:** Trame leverages libraries like Vuetify, providing a wide range of pre-built, visually appealing, and interactive UI components.
*   **Python-Centric Development:**  Because Trame is Python-based, you can build complex web applications and perform computations using Python, without needing extensive front-end web development knowledge.

## Introducing `nova-trame`

`nova-trame` simplifies the process of creating consistent and easy-to-use Trame applications. It builds upon the core Trame framework by providing a set of pre-built components, layouts, themes, and utilities that are tailored to the needs of the NOVA ecosystem.

Benefits of using `nova-trame`:

*   **Simplified UI Development:** Reduces the amount of boilerplate code required to create a Trame application.
*   **Consistent Look and Feel:** Ensures all NOVA applications have a consistent look and feel by applying a common theme and style.
*   **Reusable UI Components:** Makes it easy to use reusable UI components within your application.
*   **Integration with MVVM:** `nova-trame` works seamlessly with the `nova-mvvm` library to implement the MVVM architecture.

## Creating the UI - Key Code Snippets

Let's create a basic user interface for our fractal tool using `nova-trame` and Vuetify components. You can find the complete code for this episode in the `code/episode_5` directory. Here, we will examine the key code snippets in `fractal_view.py` and `main.py`.

**1. `FractalApp` View Class (`src/nova_tutorial/views/fractal_view.py`):**

*   **Imports**:  The `FractalApp` view starts by importing necessary classes from `nova-trame`, `trame`, and our `nova_tutorial` modules:

    ```python
    # src/nova_tutorial/views/fractal_view.py
    from nova.mvvm.trame_binding import TrameBinding
    from nova.trame import ThemedApp
    from nova.trame.view import layouts
    from trame.app import get_server
    from trame.widgets import vuetify3 as vuetify
    from nova_tutorial.view_models.fractal_view_model import FractalViewModel

    ```
    Notice the imports from `nova.trame` (like `ThemedApp`, `layouts`), `trame.app`, `trame.widgets.vuetify3`, and our existing `FractalViewModel` and `TrameBinding`.

*   **`FractalApp` Class Definition**: We define `FractalApp` as a class that inherits from `ThemedApp`.  `ThemedApp` from `nova-trame` provides a base class with a consistent NOVA theme for Trame applications:

    ```python
    class FractalApp(ThemedApp): # Inherits from nova.trame.ThemedApp for consistent styling
        def __init__(self) -> None:
            super().__init__()
            self.server = get_server(None, client_type="vue3")
            self.fractal_vm = FractalViewModel(TrameBinding(self.server.state))
            self.create_ui()
    ```
    In the `__init__` method:
    *   `super().__init__()` calls the `ThemedApp` constructor.
    *   `self.server = get_server(...)` initializes the Trame server.
    *   `self.fractal_vm = FractalViewModel(TrameBinding(self.server.state))` instantiates our `FractalViewModel`, crucially passing it a `TrameBinding` instance. This is what connects the ViewModel to the Trame UI.
    *   `self.create_ui()` calls the method that defines the user interface layout.

*   **`create_ui` method**: This method defines the structure and components of our UI using Vuetify widgets within Trame layouts:

    ```python
        def create_ui(self) -> None:
            self.state.trame__title = "NOVA Tutorial" # Set window title
            with super().create_ui() as layout: # Use themed layout
                with layout.content: # Main content area
                    with layouts.VBoxLayout(classes="ma-2"): # Vertical layout with margin
                        with vuetify.VCard(classes="pa-2"): # Card container with padding
                            with vuetify.VRadioGroup( # Radio button group for fractal type
                                v_model=("fractal_vm.fractal_type", "mandelbrot"), # Two-way binding to ViewModel
                                classes="mb-2", # Margin bottom
                            ):
                                vuetify.VRadio(label="Mandelbrot", value="mandelbrot") # Radio options
                                vuetify.VRadio(label="Julia", value="julia")
                                vuetify.VRadio(label="Random", value="random")
                                vuetify.VRadio(label="Markus", value="markus")
                            vuetify.VBtn( # Button to run the tool
                                "Run Fractal Tool",
                                click=self.fractal_vm.run_fractal_tool, # Method to call on click
                                disabled=("fractal_vm.run_button_disabled"), # Disable based on ViewModel state
                                classes="mb-2"
                            )
                            vuetify.VCardText(("fractal_vm.message")) # Display messages from ViewModel
                return layout
    ```
    Key points in `create_ui()`:
    *   `self.state.trame__title = ...`: Sets the title of the browser window for the Trame application.
    *   `with super().create_ui() as layout:`:  Creates the base UI layout using `ThemedApp`'s styling.
    *   `layouts.VBoxLayout` and `vuetify.VCard`:  Basic layout components to structure the UI vertically within a card container.
    *   `vuetify.VRadioGroup` and `vuetify.VRadio`: Creates a group of radio buttons for selecting the fractal type. **Crucially, `v_model=("fractal_vm.fractal_type", "mandelbrot")` establishes a *two-way data binding***.  Changes in the UI radio buttons will update `fractal_vm.fractal_type` in the ViewModel, and vice versa. `"mandelbrot"` sets the default value.
    *   `vuetify.VBtn`: Creates a button labeled "Run Fractal Tool".
        *   `click=self.fractal_vm.run_fractal_tool`:  Binds the button's `click` event to call the `run_fractal_tool` method in our `FractalViewModel`.
        *   `disabled=("fractal_vm.run_button_disabled")`:  **Binds the button's `disabled` state to the `run_button_disabled` property in the ViewModel**. The button will be disabled when `fractal_vm.run_button_disabled` is `True` and enabled when `False`.
    *   `vuetify.VCardText(("fractal_vm.message"))`: Displays text within the card. **Binds the content of the `VCardText` to the `message` property of the ViewModel**.  Any changes to `fractal_vm.message` will be displayed here.

**2. `main.py` - Starting the Trame Application (`src/nova_tutorial/main.py`):**

*   **Import `FractalApp`**: We import the `FractalApp` class from `nova_tutorial.views.fractal_view`:
    ```python
    # src/nova_tutorial/main.py
    from nova_tutorial.views.fractal_view import FractalApp
    ```

*   **Instantiate and Start `FractalApp`**:  In the `main()` function, we create an instance of `FractalApp` and call `app.server.start()` to launch the Trame application:

    ```python
    def main():
        app = FractalApp() # Instantiate the FractalApp (which creates the UI and ViewModel)
        app.server.start() # Start the Trame server, launching the web application

    if __name__ == "__main__":
        main()
    ```
    `app.server.start()` is the essential command to start the Trame server, which will open your web browser and display the user interface defined in `FractalApp`.

## Running the application

To run the code, use the following command in the top level of your `nova_tutorial` project:

```bash
poetry run app
```

You should now see a simple UI in your browser.

## Adding More UI Components

Let's enhance our UI by adding a few more common Vuetify components. We'll add:

*   **`VTextField`:** For text input (although not connected to backend logic in this tutorial).
*   **`VCheckbox`:** For boolean input (again, not connected to backend).
*   **`VSlider`:** For numerical input (not connected).

Modify your `src/nova_tutorial/views/fractal_view.py` to include these components within the `VCard` in the `create_ui` method:

```python
# src/nova_tutorial/views/fractal_view.py
from nova.mvvm.trame_binding import TrameBinding
from nova.trame import ThemedApp
from nova.trame.view import layouts
from trame.app import get_server
from trame.widgets import vuetify3 as vuetify
from nova_tutorial.view_models.fractal_view_model import FractalViewModel

class FractalApp(ThemedApp):
    def __init__(self) -> None:
        super().__init__()
        self.server = get_server(None, client_type="vue3")
        self.fractal_vm = FractalViewModel(TrameBinding(self.server.state))
        self.create_ui()

    def create_ui(self) -> None:
        self.state.trame__title = "NOVA Tutorial"
        with super().create_ui() as layout:
            with layout.content:
                with layouts.VBoxLayout(classes="ma-2"):
                    with vuetify.VCard(classes="pa-2"):
                        vuetify.VTextField(label="Example Text Input", classes="mb-2") # Added VTextField
                        vuetify.VCheckbox(label="Example Checkbox", classes="mb-2") # Added VCheckbox
                        vuetify.VSlider(label="Example Slider", v_model=25, classes="mb-2") # Added VSlider
                        with vuetify.VRadioGroup(
                            v_model=("fractal_vm.fractal_type", "mandelbrot"),
                            classes="mb-2",
                        ):
                            vuetify.VRadio(label="Mandelbrot", value="mandelbrot")
                            vuetify.VRadio(label="Julia", value="julia")
                            vuetify.VRadio(label="Random", value="random")
                            vuetify.VRadio(label="Markus", value="markus")
                        vuetify.VBtn(
                            "Run Fractal Tool",
                            click=self.fractal_vm.run_fractal_tool,
                            disabled=("fractal_vm.run_button_disabled"),
                            classes="mb-2"
                        )
                        vuetify.VCardText(("fractal_vm.message"))
            return layout
```

We've simply added a `VTextField`, `VCheckbox`, and `VSlider` component within the `VCard`.  These are not yet connected to the ViewModel - they are just there to demonstrate adding different UI elements.

## Running the application

To run the code, use the following command in the top level of your `nova_tutorial` project:

```bash
poetry run app
```

You should now see a UI with a text field, checkbox, slider, radio buttons, and the "Run Fractal Tool" button.

## Exercises

1.  **Explore Vuetify Components:**  Visit the Vuetify 3 component documentation ([https://vuetifyjs.com/en/components/all/](https://vuetifyjs.com/en/components/all/)). Browse through the list of available components. Identify at least three new components that you think could be useful in a scientific application UI and briefly describe their purpose.
2.  **Add a `VSelect` (Dropdown):** Add a `VSelect` component to the UI in `fractal_view.py` within the `VCard`. Make it offer a dropdown of color options (e.g., "Red", "Green", "Blue"). *(You don't need to connect it to the viewmodel.)*
3.  **Customize Component Appearance:**  Experiment with customizing the appearance of the `VBtn` component. Try changing its color, adding an icon *after* the text (e.g., using the `append-icon` prop and a Material Design Icon name), and modifying its size using Vuetify props (refer to the Vuetify documentation for `VBtn`).
