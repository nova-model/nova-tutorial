---
title: "Data Validation with Pydantic"
teaching: 20
exercises: 0
---

# 6. Data Validation with Pydantic: Ensuring Data Integrity

In this section, we will explore Pydantic, a powerful Python library for data validation and settings management. We'll delve into the benefits of data validation, how Pydantic works, and best practices for using it effectively within the NOVA framework and the MVVM architecture.

## Why Data Validation Matters

Data validation is the process of ensuring that data meets certain criteria before it's processed by your application. It's a crucial step in building robust and reliable software. Without proper data validation, your application could be vulnerable to:

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

## How Pydantic Works

Pydantic uses Python type hints to define data models. When you create an instance of a Pydantic model, Pydantic automatically validates the input data against the defined types and constraints.

Here's a simple example:

```python
from pydantic import BaseModel, Field

class User(BaseModel):
    id: int = Field(default=1, gt=0)  # id must be an integer greater than 0
    name: str = Field(default="someName", min_length=1) # name must be a string with at least one character
    email: str = Field(default="test@test.com", regex=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$") # email must be a valid email address
```

In this example, we define a `User` model with three fields: `id`, `name`, and `email`. We use type hints to specify the data type for each field (e.g., `int`, `str`) and `Field` with validation arguments to specify additional constraints (e.g., `gt=0`, `min_length=1`, `regex=...`).

When you create an instance of the `User` model, Pydantic automatically validates the input data:

```python
from pydantic import ValidationError

try:
    user = User(id=0, name="", email="invalid-email")
except ValidationError as e:
    print(e)
```

If the input data is invalid, Pydantic raises a `ValidationError` exception with detailed information about the validation errors.

## Where to Perform Validation: Model vs. ViewModel

In the MVVM architecture, the question arises: where should data validation be performed? Should it be done in the Model or the ViewModel?

*   **Model Validation:** Validating data in the Model ensures that the underlying data is always in a valid state. This is especially important for data that is stored in a database or used by other parts of the application. However, Model validation is not always UI-specific.

*   **ViewModel Validation:** Validating data in the ViewModel allows you to perform UI-specific validation, such as checking that a required field is not empty or that a value falls within a certain range. ViewModel validation is also useful for providing immediate feedback to the user about validation errors.

In general, it's a good practice to perform both Model and ViewModel validation. Model validation ensures data integrity at the data level, while ViewModel validation provides a better user experience by providing immediate feedback and preventing invalid data from being passed to the Model. Pydantic supports both.

In the context of our NOVA tutorial, here's how we can apply this:

*   **NDIP Interactions (Model):** When using `nova-galaxy` to interact with NDIP, validate the data being sent to NDIP in the Model to ensure it conforms to the NDIP API requirements.

*   **UI Input (ViewModel):** When the user enters data in the UI, validate the data in the ViewModel to provide immediate feedback to the user.

## Pydantic and `nova-trame` Input Validation

One of the great features of `nova-trame` is that it leverages the validation attributes of Pydantic models to automatically create validation routines for Vuetify UI elements. Let's walk through what that looks like in code.

First, let's assume you have the following model:

```python
from pydantic import BaseModel, Field

class SettingsModel(BaseModel):
    port: int = Field(default=8080, gt=0, lt=65536, title="Port Number", description="The port to listen on.")
```

Then in your view, you create the following InputField:

```python
from nova.trame.view.components import InputField

InputField(v_model="settings.port")
```

Notice how you don't need to pass any attributes to `InputField` other than `v_model`. The `InputField` automatically retrieves the `title` and attempts to retrieve other information.

The InputField performs automatic validation for this field. If you enter an invalid port number into the InputField, the InputField will change state to invalid and the label will turn red.

In that fashion, the `InputField` seamlessly pulls information from your code's data model and displays errors to the user.