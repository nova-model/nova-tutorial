```markdown
# Integrating Trame with `nova-trame`

In this section, we will introduce Trame and the `nova-trame` library. We'll cover the benefits of Trame and how `nova-trame` simplifies the development of Trame applications. Finally, we'll integrate with `nova-trame` and build a simple UI.

## Introduction to Trame

Trame is a powerful Python framework for building interactive web-based user interfaces and visualizations. It enables developers to create dynamic applications using a declarative approach, which means you focus on *what* the UI should look like, rather than *how* to implement the UI. It leverages other powerful open source libraries like Vue.js, Vuetify, and VTK.

Key Features and Benefits of Trame:

*   **Declarative UI:** Describe your user interfaces using Python code. Trame takes care of translating that code into a functional web application.
*   **Interactive Applications:** Create dynamic UIs with real-time updates using Trame's data binding capabilities. When the data in your viewmodel changes, the UI changes as well.
*   **Web-Based:** Trame applications are web applications, accessible from any modern web browser, making them easy to deploy and share.
*   **Extensible:** Trame can be extended using third-party libraries like Vuetify to create rich user interfaces.
*  **Python Based:** Because Trame leverages python, you can create your own components and also perform complex calculations directly in python rather than relying on javascript.

Trame allows for creation of complex web based applications while not requiring users to have knowledge of front end web development.

## Introducing `nova-trame`

`nova-trame` simplifies the process of creating consistent and easy-to-use Trame applications. It builds upon the core Trame framework by providing a set of pre-built components, layouts, themes, and utilities that are tailored to the needs of the NOVA ecosystem.

Benefits of using `nova-trame`:

*   **Simplified UI Development:** Reduces the amount of boilerplate code required to create a Trame application.
*   **Consistent Look and Feel:** Ensures all NOVA applications have a consistent look and feel by applying a common theme and style.
*  **Reusable Components:** Makes it easy to use reusable UI components within your application.
*   **Integration with MVVM:** `nova-trame` works seamlessly with the `nova-mvvm` library to implement the MVVM architecture.

## Creating the UI

Let's create a new file named `src/nova_tutorial/views/fractal_view.py` with the following contents:

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

This code will create a layout, card, radio buttons, and a button for you. Note that the `v-model` on the radio buttons is bound to the `fractal_vm.fractal_type` variable, and the button is bound to the `fractal_vm.run_fractal_tool` method.
## Running the application

Finally, to run this application, let's update our `src/nova_tutorial/main.py` file as follows:

```python
# src/nova_tutorial/main.py
from nova_tutorial.views.fractal_view import FractalApp

def main():
    app = FractalApp()
    app.server.start()

if __name__ == "__main__":
    main()
```

Key Changes:

*   **`FractalApp` Class:** This class was added to act as a container for the ui and view model.
*   **UI Components:** The `create_ui` method in `FractalApp` has been populated with Vuetify UI components.
*   **MVVM Integration:** `TrameBinding` has been incorporated.
*   **View Model Usage:** The view model is now being used to update state variables and call methods.
*  **Updated `main.py`:** We now are calling the `FractalApp` in the main file to start the trame server.

## Running the application

To run the code, use the following command in the top level of your `nova_tutorial` project:

```bash
poetry install
poetry run app
```

You should now see a simple UI in your browser.
