---
title: "Advanced Data Validation with Pydantic"
teaching: 60
exercises: 0
---

::::::::::::::::::::::::::::::::::::::: objectives

- Represent data model using Pydantic library.
- Define nested Pydantic models to represent complex data structures.
- Implement custom validation logic for a single field.
- Implement custom validation logic for the whole model.
- Use Pydantic models in NOVA framework.

::::::::::::::::::::::::::::::::::::::::::::::::::

:::::::::::::::::::::::::::::::::::::::: questions

- Why is data validation important?
- What is Pydantic and how it works?
- How can I represent complex data structures with nested relationships using Pydantic?
- How can I enforce validation rules that go beyond basic type checking using Pydantic?
- How do I use Pydantic models in NOVA framework?

::::::::::::::::::::::::::::::::::::::::::::::::::

# 6. Advanced Data Validation with Pydantic: Ensuring Data Integrity

In this section, we will explore Pydantic, a powerful Python library for data validation and settings management. We\'ll delve into the benefits of data validation, how Pydantic works, and best practices for using it effectively within the NOVA framework and the MVVM architecture.

The complete code for this episode is available in the `code/episode_6` directory.

## Why Data Validation Matters

Data validation is the process of ensuring that data meets certain criteria before it\'s processed by your application. It\'s a crucial step in building robust and reliable software. Without proper data validation, your application could be vulnerable to:

*   **Unexpected Errors:** Invalid data can cause your application to crash or produce incorrect results.
*   **Security Vulnerabilities:** Malicious users can exploit the lack of data validation to inject harmful data into your application, leading to security breaches.
*   **Data Corruption:** Invalid data can corrupt your data stores, leading to data loss or inconsistency.
*   **Integration Issues:** When interacting with external systems or APIs, data validation ensures that your data conforms to the expected format and constraints.

Data validation helps you:

*   **Improve Data Quality:** By enforcing data constraints, you ensure that your application works with clean and consistent data.
*   **Enhance Application Reliability:** By preventing invalid data from being processed, you reduce the risk of errors and crashes.
*   **Strengthen Security:** By sanitizing user input and validating data from external sources, you protect your application from security threats.

## Introduction to Pydantic

Pydantic is a Python library that provides a powerful and elegant way to define data models and enforce data validation. It uses Python type hints to define the structure of your data and automatically validates data against these types at runtime.

Key Features of Pydantic:

*   **Data Validation:** Automatically validates data types and constraints, ensuring data integrity. Pydantic supports a wide range of validation options, including type checking, length constraints, regular expressions, custom validators, and more.
*   **Clear Data Structures:** Defines data models in a clear and readable way using Python type hints. Pydantic models are easy to understand and maintain.
*   **Serialization and Deserialization:** Easily serializes data to and from standard formats like JSON. This is useful for interacting with APIs and other external systems.
*   **Settings Management:** Can be used to manage application settings and configuration, providing a centralized and type-safe way to access configuration values.
*   **Improved Code Readability:** Makes code easier to understand and maintain by explicitly defining data models. Type hints make it clear what type of data is expected for each field.


## Create a new CLI project

Let\'s start by setting up a new application from the template. 

To clone the template application, run the following command:

```bash
copier copy https://code.ornl.gov/ndip/project-templates/nova-application-template.git advanced_pydantic
```

This command will download the template to a directory called `advanced_pydantic`. Copier will prompt you with a series of questions. Please answer the questions as follows:

*   **What is your project name?**

    > Enter `Advanced Pydantic`

*   **All other questions**

    > Press enter to accept the default.

After that, go into the created folder and install project dependencies:

```bash
cd advanced_pydantic
poetry install
```


## How Pydantic Works

Pydantic uses Python type hints to define data models. When you create an instance of a Pydantic model, Pydantic automatically validates the input data against the defined types and constraints.

1. Create a User Model (`src/advanced_pydantic/main.py`) (Modify):

```python
from pydantic import BaseModel, Field

class User(BaseModel):
    id: int = Field(default=1, gt=0)  # id must be an integer greater than 0
    name: str = Field(default="someName", min_length=1) # name must be a string with at least one character
```

In this example, we define a `User` model with two fields: `id` and `name`. We use type hints to specify the data type for each field (e.g., `int`, `str`) and `Field` with validation arguments to specify additional constraints (e.g., `gt=0`, `min_length=1`, ...).

When you create an instance of the `User` model, Pydantic automatically validates the input data.

2. Create an instance of a User (`src/advanced_pydantic/main.py`) (Modify):

```python
from pydantic import ValidationError

def main() -> None:  
    try:
        user = User(id=0, name="")
        print(user)
    except ValidationError as e:
        print(e)
```

and run it with 
```bash
poetry run app
```


If the input data is invalid, Pydantic raises a `ValidationError` exception with detailed information about the validation errors.


## Using Pydantic to represent more complex data structures

When working with structured data, it\'s common to have nested objects. For example, a User model from the above example might have multiple Address entries. In Pydantic, we can achieve this by creating nested models.

1. Creating the Address Model (`src/advanced_pydantic/main.py`) (Modify).

The Address model represents a simple address with three fields:

- street: A string with a minimum length of 3 and a maximum of 50.
- city: A string with a minimum length of 2 and a maximum of 30.
- zip_code: A string that must match a 5-digit ZIP code format.
- type: A string that must be "home" or "work".

```python
from typing import Literal
from pydantic import BaseModel, Field

class Address(BaseModel):
    street: str = Field(min_length=3, max_length=50)
    city: str = Field(min_length=2, max_length=30)
    zip_code: str = Field(pattern=r"^\d{5}$")  # US ZIP code validation
    type: Literal["home", "work"] = Field()
```

2. Using the Address Model as a Nested Field (`src/advanced_pydantic/main.py`) (Modify).

Update the User model so that it now contains:

- id: An integer that must be greater than 0 (default is 1).
- name: A required string with at least 1 character (default is "someName").
- addresses: A list of Address models, requiring at least one address.

```python    
from typing import List

class User(BaseModel):
    id: int = Field(default=1, gt=0)
    name: str = Field(default="someName", min_length=1)
    addresses: List[Address] = Field(min_length=1)
```

3. Test the model (`src/advanced_pydantic/main.py`) (Modify).

```python    
def main() -> None:
   
    # Example input
    user_data = {
        "id": 1,
        "name": "Alice",
        "addresses": [{
            "street": "123 Main St",
            "city": "New York",
            "zip_code": "10001",
            "type": "home"
        }]
    }
    
    user = User.model_validate(user_data)
    print(user)

```

and run it with 
```bash
poetry run app
```

::::::::::::::::::::::::::::::::::::::::: callout
For easier integration with the NOVA framework, where model field information is used for displaying and validating GUI elements, we recommend avoiding overly complex nested structures. In particular, lists of lists are currently not supported.
::::::::::::::::::::::::::::::::::::::::::::::::::

## Implement custom validation logic for a single field

Sometimes, simple validation like checking the minimum length is not enough. In such cases, you can write a custom validation function for a specific field.

For example, let\'s say we have a User model where only even IDs are allowed. We can enforce this constraint using the `@field_validator decorator`.

4. Using the `@field_validator decorator` (`src/advanced_pydantic/main.py`) (Modify):

```python
from pydantic import BaseModel, Field, field_validator

class User(BaseModel):
    id: int = Field(default=1, gt=0)
    name: str = Field(default="someName", min_length=1)

    @field_validator("id", mode="after")  
    @classmethod
    def is_even(cls, value: int) -> int:
        if value % 2 == 1:
            raise ValueError(f"{value} is not an even number")
        return value
    
def main() -> None:      
    # Example input
    user_data = {
        "id": 1,    
        "name": "Alice",
    }
    
    user = User.model_validate(user_data)
    print(user)
```

This code will raise a ValueError because the provided id (1) is not an even number.


::::::::::::::::::::::::::::::::::::::::: callout
Note that we used the mode="**after**" option for the validator. This ensures that our custom validation runs after Pydantic\'s internal validation (in our example example, checking that the id is an integer and greater than 0). Alternatively, you can use mode="**before**", where custom validation occurs before the internal validation. Validators in the after mode are generally more type-safe, making them easier to implement.
::::::::::::::::::::::::::::::::::::::::::::::::::


## Implement custom validation logic for the whole model

In some cases, you may need to validate the entire model, not just individual fields. This can be done by writing a custom validation function for the whole model using the `@model_validator` decorator.

For example, let\'s say we have a User model where the name and id must meet specific conditions together. For instance, we only allow users with even IDs to have names that start with a capital letter. We can enforce this logic using a @model_validator.

5. Using the `@model_validator decorator` (`src/advanced_pydantic/main.py`) (Modify):

```python
from pydantic import BaseModel, Field, model_validator
from typing_extensions import Self

class User(BaseModel):
    id: int = Field(default=1, gt=0)
    name: str = Field(default="someName", min_length=1)

    @model_validator(mode='after')
    def check_name_for_even_id(self) -> Self:
        if self.id % 2 == 0 and not self.name[0].isupper():
            raise ValueError(f"Name must start with a capital letter when the ID is even.")
        
        return self

def main() -> None:   
    # Example input
    user_data = {
        "id": 2,    
        "name": "alice",  # Name starts with lowercase, should raise an error
    }
    
    user = User.model_validate(user_data)
    print(user)
```

This code will raise a ValueError because the name ("alice") does not start with a capital letter, while the id is even.

## Create a simple Trame application

Now, let\'s create a simple Trame-based GUI application.

To clone the template application, run the following command:

```bash
copier copy https://code.ornl.gov/ndip/project-templates/nova-application-template.git pydantic_mvvm
```

This command will download the template to a directory called `pydantic_mvvm`. Copier will prompt you with a series of questions. Please answer the questions as follows:

*   **What is your project name?**

    > Enter `Trame with Pydantic`

*   **What is your Python package name (use Python naming conventions)?**

    > Press enter to accept the default.

*   **Do you want to install Mantid for your project?**

    > Enter `n`

*   **Are you developing a GUI application using MVVM pattern?**

    > Enter `y`

*   **Which library will you use?**

    > Select `Trame`

*   **Do you want a template with multiple tabs?**

    > Enter `n`

*   **Publish to PyPI?**

    > Enter `n`

*   **Publish documentation to readthedocs.io?**

    > Enter `n`

After that, go into the created folder and install project dependencies:

```bash
cd pydantic_mvvm
poetry install
```


## Using Pydantic models in NOVA framework

One of the great features of the NOVA Framework is that it allows an application to leverage Pydantic models to automatically validate UI elements. Let\'s walk through what that looks like in code.

1. First, let\'s add the following Model (`src/trame_with_pydantic/app/models/settings.py`) (Create):

```python
from pydantic import BaseModel, Field

class SettingsModel(BaseModel):
    port: int = Field(default=8080, gt=0, lt=65536, title="Port Number", description="The port to listen on.", examples=["12345"])
```

2. Create a binding for the model (`src/trame_with_pydantic/app/view_models/main.py`) (Modify):

In your ViewModel, create a binding for this Model and clean up the code created by the template engine, we don't need it for this example):

```python
from typing import Any, Dict
from nova.mvvm.interface import BindingInterface

from ..models.settings import SettingsModel

class MainViewModel:
    def __init__(self, _, binding: BindingInterface):
        self.settings = SettingsModel()
        self.settings_bind = binding.new_bind(self.settings)        
```

3. In your view, remove all other fields and add the following InputField (`src/trame_with_pydantic/app/views/main.py`) (Modify):

```python

    def __init__(self) -> None:
        ....
        self.view_model.settings_bind.connect("settings")
        ....

...
    with layout.content:
        with vuetify.VRow(align="center", classes="mt-4"):
            InputField(v_model="settings.port")
```

Notice how you don\'t need to pass any attributes to `InputField` other than `v_model`. The `InputField` automatically retrieves the `title`, `description` and `examples`. The values are used for label, hint and empty value.

The InputField also performs automatic validation for this field. If you enter an invalid port number into the InputField, the InputField will change state to invalid and the label will turn red.

In that fashion, the `InputField` seamlessly pulls information from your code\'s data model and displays errors to the user.

### Using callbacks in ViewModel to react to validation errors

Sometimes, you may want to respond to UI validation errors beyond just marking a field as invalid (which happens automatically). In such cases, you can add a callback to the `new_bind` function.

4. Using callbacks with `new_bind` (`src/trame_with_pydantic/app/view_models/main.py`) (modify):

```python
class MainViewModel:
    def __init__(self, _, binding: BindingInterface):
        ...
        self.settings_bind = binding.new_bind(self.settings, callback_after_update=self.process_settings_change)

    def process_settings_change(self, results: Dict[str, Any]) -> None:
        if results["error"]:
            print(f"error in fields {results['errored']}, model not changed")
        else:
            print(f"model fields updated: {results['updated']}")

```

The function will receive a dictionary containing lists of updated or invalid fields. Note that if a validation error occurs, the model will not be updated, leading to a discrepancy between the values displayed in the UI and those in the model.

:::::::::::::::::::::::::::::::::::::::  challenge
**Model validation**
Change the model validation rule so that it does not allow user `alice`.
::::::::::::::::::::::::::::::::::::::::::::::::::

:::::::::::::::::::::::::::::::::::::::  challenge
**Pydantic Field**
Add another Pydantic field - a float value that should be positive, to the model.
::::::::::::::::::::::::::::::::::::::::::::::::::


:::::::::::::::::::::::::::::::::::::::  challenge
**Value auto fix**
In the GUI application, set the port to the default value if a user enters an incorrect value in the interface.
::::::::::::::::::::::::::::::::::::::::::::::::::

:::::::::::::::::::::::::::::::::::::::: keypoints
- Data Validation has many key benefits, such as protecting against errors, data corruption, and vulnerabilities. 
- Pydantic is a powerful Python library used to define data models and enforce data validation.
- Pydantic supports complex data structures and custom data validation logic.
- The NOVA Framework supports Pydantic models to automatically validate UI elements.
::::::::::::::::::::::::::::::::::::::::::::::::::

## References

*   **Nova Documentation**: https://nova-application-development.readthedocs.io/en/latest/
*   **nova-galaxy documentation**: https://nova-application-development.readthedocs.io/projects/nova-galaxy/en/latest/
*   **nova-trame documentation**: https://nova-application-development.readthedocs.io/projects/nova-trame/en/stable/
*   **nova-mvvm documentation**: https://nova-application-development.readthedocs.io/projects/mvvm-lib/en/latest/
*   **Calvera documentation**: https://calvera-test.ornl.gov/docs/