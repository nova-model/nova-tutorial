---
title: "Advanced Data model Validation Using Pydantic"
teaching: 10
exercises: 3
---

# Advanced Data Model Validation Using Pydantic

In this section, we will delve deeper into Pydantic and explore more advanced data validation techniques. We will expand upon the basic Pydantic introduction from Day 1 and learn how to define more complex data models and validation rules.

## Advanced Pydantic Features

Building upon our basic understanding of Pydantic, let's explore some advanced features that make it even more powerful for data validation and management:

*   **Nested Models:** Pydantic allows you to define models that are nested within each other. This is useful for representing complex data structures.
*   **List and Dictionary Validation:** Pydantic can validate lists and dictionaries, ensuring that the elements within them conform to specific types or models.
*   **Custom Validation:** Pydantic provides mechanisms for defining custom validation functions to enforce business-specific rules beyond basic type checking.
*   **Data Transformation:** Pydantic can automatically transform data during validation (e.g., converting strings to dates, cleaning up whitespace).

## Nested Pydantic Models

Let's imagine we want to represent more complex input for our fractal tool.  Suppose we want to group parameters related to the fractal's appearance into a nested model.  Modify your `src/nova_tutorial/view_models/fractal_view_model.py` to include a nested model like `FractalAppearance`:

```python
# src/nova_tutorial/view_models/fractal_view_model.py
import os
from nova.galaxy import Nova, Parameters, Tool
from nova.mvvm.interface import BindingInterface
from pydantic import BaseModel, ValidationError
from typing import Literal, Optional

class FractalAppearance(BaseModel): # Nested Model
    color_palette: Optional[Literal["viridis", "magma", "plasma"]] = "viridis" # Optional field with default

class FractalToolInput(BaseModel):
    fractal_type: Literal["mandelbrot", "julia", "random", "markus"]
    appearance: FractalAppearance = FractalAppearance() # Nested model as a field


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

    @property
    def fractal_type(self):
        return self._fractal_type

    @fractal_type.setter
    def fractal_type(self, value):
        self.set_fractal_type(value)
```

We've added `FractalAppearance` as a nested model and included it as a field in `FractalToolInput`.  Note that `color_palette` is optional and has a default value.

## Custom Validation

Pydantic allows for custom validation logic using validator decorators.  Let's add a custom validator to `FractalToolInput` to ensure that if `fractal_type` is "julia", then `color_palette` must be specified as "plasma".  *(This is a contrived example for demonstration purposes.)*

Add the following validator to the `FractalToolInput` model in `src/nova_tutorial/view_models/fractal_view_model.py`:

```python
# ... inside FractalToolInput class ...
    @pydantic.model_validator(mode='after')
    def check_julia_palette(self) -> 'FractalToolInput':
        if self.fractal_type == "julia" and self.appearance.color_palette != "plasma":
            raise ValueError("For 'julia' fractals, color_palette must be 'plasma'.")
        return self
```

You'll also need to import `pydantic` at the top of the file: `import pydantic`.

This validator function is decorated with `@pydantic.model_validator(mode='after')`, which means it runs *after* the basic field validation. It checks the condition and raises a `ValueError` if the rule is violated.

## Running the application

To run the code, use the following command in the top level of your `nova_tutorial` project:

```bash
poetry install
poetry run app
```

This will still run the application, but now Pydantic models with nested structures and custom validation are defined.

## Exercises

1.  **Trigger Nested Model Validation:**  Modify the `set_fractal_type` method to also set a value for `appearance.color_palette` when the `fractal_type` is set.  Try setting an invalid `color_palette` value (e.g., `"invalid_palette"`). What validation error do you observe?
2.  **Trigger Custom Validator:** Modify the `set_fractal_type` method to set `fractal_type` to `"julia"` and `appearance.color_palette` to `"viridis"`. Run the application. What validation error do you see now? Why?
3.  **Explore Pydantic Validators:** Refer to the Pydantic documentation on validators ([https://docs.pydantic.dev/latest/usage/validators/](https://docs.pydantic.dev/latest/usage/validators/)). Identify at least two other types of validators (e.g., `@field_validator`, `@root_validator`).  Briefly describe their purpose and how they differ from `@model_validator`.