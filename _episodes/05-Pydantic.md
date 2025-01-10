```markdown
# Pydantic and Model Validation

In this section, we will introduce Pydantic, a library for data validation and settings management using Python type hints. We will discuss the core features and benefits of Pydantic and then integrate it into our existing project to validate user inputs.

## Introduction to Pydantic

Pydantic is a data validation and settings management library that enforces type hints at runtime. With Pydantic, you can define data models using standard Python type hints, and Pydantic automatically validates the data against those models. It also provides tools for data serialization and parsing.

Pydantic plays a critical role in ensuring that the data in our applications is consistent, well-formed, and reliable.

## Core Concepts and Benefits

*   **Type Hinting:** Pydantic leverages Python's type hints to define data models. It understands basic types (int, str, float, bool), as well as more complex types (lists, dictionaries, sets, and other Pydantic models). This makes it very expressive, and intuitive for python developers to use.
*   **Data Validation:** Pydantic automatically validates incoming data against the defined models. If the data does not conform to the expected types or constraints, Pydantic raises a validation error, which can be handled by the application.
*   **Data Serialization:** Pydantic allows for easy serialization of models to JSON, dictionaries, and other formats.
*   **Settings Management:** Pydantic can be used to manage application settings and configuration by defining a Pydantic model for the settings.

Using Pydantic can improve data quality, increase developer productivity, and reduce common sources of errors.

## Defining Pydantic Models

To use Pydantic, we first need to define a Pydantic model. A model is a python class that inherits from `pydantic.BaseModel`, and the model is defined by setting the attributes and types in that class.

```python
from pydantic import BaseModel
from typing import Literal

class FractalToolInput(BaseModel):
    fractal_type: Literal["mandelbrot", "julia", "random", "markus"]
```

## Using Pydantic Validation

Once we have a model, we can use it to validate data by creating an instance of that model. If the data does not conform to the model, Pydantic will throw a validation error.

```python
from pydantic import BaseModel, ValidationError
from typing import Literal

class FractalToolInput(BaseModel):
    fractal_type: Literal["mandelbrot", "julia", "random", "markus"]

try:
    input = FractalToolInput(fractal_type="invalid")
except ValidationError as e:
    print(f"Validation Error: {e}")
```

## Integrating with Our Code

Now, let's integrate Pydantic into our `src/nova_tutorial/view_models/fractal_view_model.py` file.

```python
# src/nova_tutorial/view_models/fractal_view_model.py
import os
from nova.galaxy import Nova, Parameters, Tool
from nova.mvvm.interface import BindingInterface
from pydantic import BaseModel, ValidationError
from typing import Literal

class FractalToolInput(BaseModel):
    fractal_type: Literal["mandelbrot", "julia", "random", "markus"]


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


    def set_fractal_type(self, fractal_type: str):
        try:
            FractalToolInput(fractal_type=fractal_type)
        except ValidationError as e:
             self._message = f"Validation Error: {e}"
             self.message_bind.update_in_view(self._message)
             return
        self._fractal_type = fractal_type
        self.fractal_type_bind.update_in_view(self._fractal_type)

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
            params.add_input(name="fractal_type", value=self._fractal_type)
            
            with nova.connect() as galaxy_connection:
                data_store = galaxy_connection.create_data_store(name="fractal_store")
                tool.run(data_store, params)
                # Datastore is deleted after function exists
            self._message = "Fractal tool finished successfully."
        except Exception as e:
            self._message = f"Error running fractal tool: {e}"
        finally:
            self.message_bind.update_in_view(self._message)
            self._run_button_disabled = False
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

**Key changes:**

*   **`FractalToolInput` Model:**  A `FractalToolInput` Pydantic model is defined. It enforces that `fractal_type` must be one of the four valid literal options using the `Literal` type.
*   **Validation in `set_fractal_type`:** The `set_fractal_type` method now validates the new value using the model and will reject the update if it fails.

## Running the application

To run the code, use the following command in the top level of your `nova_tutorial` project:

```bash
poetry install
poetry run app
```

This will still produce the same output to the console as before, but now the viewmodel is enforcing type correctness on the input.
