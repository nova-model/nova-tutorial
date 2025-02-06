---
title: "Web-based User Interface Development with Trame"
teaching: 20
exercises: 3
---

# 5. Web-based User Interface Development with Trame

In this section, we will dive into Trame and the `nova-trame` library to build interactive web-based user interfaces for our NOVA applications. We\'ll explore how `nova-trame` simplifies UI development within the NOVA ecosystem and how to use common layout components.

## Introduction to Trame

Trame is a powerful Python framework for building interactive web applications and visualizations. It lets you create UIs declaratively using Python, eliminating the need for complex JavaScript and front-end web development. Trame handles the complexities of creating a dynamic web application, allowing you to focus on your application\'s logic.

Key Features and Benefits of Trame:

*   **Declarative UI:** Define your user interfaces using Python code. You describe *what* the UI should be, not *how* to implement it using web technologies. This significantly simplifies UI development.
*   **Interactive Applications:** Create dynamic UIs with real-time updates using Trame\'s data binding capabilities. Changes in your ViewModel automatically reflect in the UI, and user interactions in the UI can update the ViewModel.
*   **Web-Based and Accessible:** Trame applications are standard web applications, accessible from any modern web browser. This makes them easy to deploy and share with colleagues and users.
*   **Extensible and Rich UI Components:** Trame leverages libraries like Vuetify, providing a wide range of pre-built, visually appealing, and interactive UI components. Vuetify follows the Material Design specification, ensuring a modern and consistent look and feel.
*   **Python-Centric Development:** Build complex web applications and perform computations using Python, without needing extensive front-end web development knowledge. This allows you to leverage your existing Python skills.

## Introducing `nova-trame`

`nova-trame` simplifies the process of creating consistent and easy-to-use Trame applications within the NOVA framework. It builds upon the core Trame framework by providing pre-built components, layouts, themes, and utilities tailored for the NOVA ecosystem.

Benefits of using `nova-trame`:

*   **Simplified UI Development:** Reduces the boilerplate code required to create a Trame application. `nova-trame` provides abstractions and helpers that streamline common UI tasks.
*   **Consistent Look and Feel:** Ensures all NOVA applications have a consistent look and feel by applying a common theme and style based on the NOVA design guidelines. This helps users easily recognize and use NOVA applications.
*   **Reusable UI Components:** Makes it easy to use reusable UI components within your application. You can create custom components and share them across multiple NOVA applications.
*   **Integration with MVVM:** `nova-trame` works seamlessly with the `nova-mvvm` library to implement the MVVM architecture. This simplifies the process of connecting your UI to your application logic.

## Key `nova-trame` Components

`nova-trame` provides several key components that simplify UI development. Here are some of the most important:

*   **`InputField`:** This component simplifies the creation of various input fields (text fields, dropdowns, checkboxes, etc.). It automatically integrates with Pydantic models to load labels, hints, and validation rules, reducing the amount of code you need to write.  It also supports debouncing and throttling for improved performance.
*   **Layout Components:** `nova-trame` provides layout components that help you structure your UI. These components are based on CSS Flexbox and Grid layouts, making it easy to create responsive and visually appealing UIs. The main layout components include:
    *   **`GridLayout`:** Creates a grid with a specified number of columns. You can use `GridLayout` to arrange your UI elements in a structured grid layout.
    *   **`VBoxLayout`:** Creates an element that vertically stacks its children. Use `VBoxLayout` to arrange UI elements in a vertical column.
    *   **`HBoxLayout`:** Creates an element that horizontally stacks its children. Use `HBoxLayout` to arrange UI elements in a horizontal row.

Let\'s explore these components in more detail:

### `InputField`

The `InputField` component simplifies creating different types of input fields in your UI. It can create text fields, dropdowns (select), checkboxes, and more, all with a consistent look and feel. A key advantage of `InputField` is its automatic integration with Pydantic models. If the `v_model` references a Pydantic model field, `InputField` can automatically:

*   **Load the label:** Use the `title` attribute from the Pydantic field as the input field\'s label.
*   **Display a hint:** Use the `description` attribute from the Pydantic field as a help text or hint for the input field.
*   **Apply validation rules:** Automatically generate validation rules based on the Pydantic field\'s type and constraints.

This integration significantly reduces the amount of boilerplate code you need to write for input fields.

The `InputField` also provides debouncing and throttling features that can improve application performance. These features are useful when dealing with user input that triggers frequent updates to the Trame state.

### Layout Components: `GridLayout`, `VBoxLayout`, and `HBoxLayout`

`nova-trame` provides several layout components that make it easy to structure your UI:

*   **`GridLayout`:** Creates a grid layout with a specified number of columns. This is useful for arranging UI elements in a structured grid. You can use the `row_span` and `column_span` attributes to control how many rows and columns each element spans.

    ```python
    from nova.trame.view import layouts
    from trame.widgets import vuetify3 as vuetify

    with layouts.GridLayout(columns=2):
        vuetify.VTextField(label="First Name")
        vuetify.VTextField(label="Last Name")
        vuetify.VTextField(label="Email")
        vuetify.VTextField(label="Phone Number")
    ```

    This code creates a grid with two columns and arranges the text fields in the grid.

*   **`VBoxLayout`:** Creates a vertical box layout, stacking its children vertically. This is useful for creating simple vertical layouts.

    ```python
    from nova.trame.view import layouts
    from trame.widgets import vuetify3 as vuetify

    with layouts.VBoxLayout():
        vuetify.VTextField(label="Address Line 1")
        vuetify.VTextField(label="Address Line 2")
        vuetify.VTextField(label="City")
    ```

    This code creates a vertical layout and stacks the text fields vertically.

*   **`HBoxLayout`:** Creates a horizontal box layout, stacking its children horizontally. This is useful for creating simple horizontal layouts.

    ```python
    from nova.trame.view import layouts
    from trame.widgets import vuetify3 as vuetify

    with layouts.HBoxLayout():
        vuetify.VTextField(label="First Name")
        vuetify.VTextField(label="Last Name")
    ```

    This code creates a horizontal layout and stacks the text fields horizontally.

By combining these layout components, you can create complex and responsive UI layouts.

## Adding More UI Components to the Sample Tabs

Now, let\'s add some UI components to the Sample Tabs in our application to demonstrate how to use these components. We\'ll modify the `sample_tab_1.py` and `sample_tab_2.py` files to include these components.

**1. `nova_tutorial/views/sample_tab_1.py` (Modify):**

We\'ll add an `InputField` and a `VBoxLayout` to this tab.

```python
"""Module for the Sample Tab 1."""

from nova.trame.view.components import InputField
from nova.trame.view import layouts
from trame.widgets import vuetify3 as vuetify

class SampleTab1:
    """Sample tab 1 view class. Renders text input for username."""

    def __init__(self) -> None:
        self.create_ui()

    def create_ui(self) -> None:
        with layouts.VBoxLayout(classes="ma-2"):
            InputField(v_model="config.username", label="Username")
            vuetify.VCheckbox(label="Remember me")
```

**2. `nova_tutorial/views/sample_tab_2.py` (Modify):**

We\'ll add a `GridLayout` and an `InputField` to this tab.

```python
"""Module for the Sample Tab 2."""

from nova.trame.view.components import InputField
from nova.trame.view import layouts
from trame.widgets import vuetify3 as vuetify

class SampleTab2:
    """Sample tab 2 view class. Renders text input for user password."""

    def __init__(self) -> None:
        self.create_ui()

    def create_ui(self) -> None:
        with layouts.GridLayout(columns=2, classes="ma-2"):
            InputField(v_model="config.password", label="Password", type="password")
            vuetify.VSlider(label="Volume")
```

In `SampleTab1`, we\'ve used a `VBoxLayout` to vertically stack the `InputField` and `VCheckbox` components. In `SampleTab2`, we\'ve used a `GridLayout` to arrange the `InputField` and `VSlider` components in a two-column grid.

## Running the application

To run the code, use the following command in the top level of your `nova_tutorial` project:

```bash
poetry run start
```

You should now see the simple UI. When you click the "Sample Tab 1" and "Sample Tab 2" tabs, you should now see the updated content with the new UI components.

## Exercises

1.  **Explore the `InputField` Component:** Modify the `InputField` component in `SampleTab1` to automatically retrieve the label, hint, and validation rules from a Pydantic model field. Create a simple Pydantic model with a `username` field with a `title`, `description`, and `min_length` constraint.
2.  **Create a Complex Layout:** Combine `GridLayout`, `VBoxLayout`, and `HBoxLayout` components to create a more complex UI layout in `SampleTab2`. Try creating a layout with a header, a sidebar, and a main content area.
3.  **Customize Component Appearance:** Experiment with customizing the appearance of the Vuetify components using the various props and styles available. Try changing the color, size, font, and other visual attributes of the components. Refer to Vuetify\'s component documentation for details.

## References

*   **Nova Documentation**: https://nova-application-development.readthedocs.io/en/latest/
*   **nova-galaxy documentation**: https://nova-application-development.readthedocs.io/projects/nova-galaxy/en/latest/
*   **nova-trame documentation**: https://nova-application-development.readthedocs.io/projects/nova-trame/en/stable/
*   **nova-mvvm documentation**: https://nova-application-development.readthedocs.io/projects/mvvm-lib/en/latest/
*   **Vuetify Documentation**: https://vuetifyjs.com/en/
```
