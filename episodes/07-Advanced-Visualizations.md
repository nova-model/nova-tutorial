---
title: "Advanced Visualizations"
teaching: 10
exercises: 1
---

::::::::::::::::::::::::::::::::::::::: objectives

- Describe the purpose of Plotly for interactive 2D charts.
- Explain how to integrate Plotly charts into Trame applications using `trame-plotly`.
- Describe the purpose of PyVista for interactive 3D visualizations.
- Explain how to integrate PyVista visualizations into Trame applications using `trame-vtk`.
- Explain how to work directly with VTK for 3D visualizations within Trame applications.
- Understand the basic boilerplate code required to set up a VTK rendering pipeline in Trame.

::::::::::::::::::::::::::::::::::::::::::::::::::

:::::::::::::::::::::::::::::::::::::::: questions

- How can I create interactive 2D charts in my NOVA application?
- How can I integrate Plotly charts into Trame applications?
- How can I create interactive 3D visualizations in my NOVA application?
- What are the advantages and disadvantages of using PyVista vs. VTK for 3D visualizations?
- How can I integrate PyVista visualizations into Trame applications?
- How can I work directly with VTK for more advanced 3D visualizations in Trame?
- What are the key components of a VTK rendering pipeline?

::::::::::::::::::::::::::::::::::::::::::::::::::

# Advanced Visualizations

In this section, we will look at a selection of the libraries that integrate well with Trame for producing more sophisticated visualizations of your data. Specifically, we will look at Plotly for interactive 2D charts, PyVista for interactive 3D visualizations, and VTK for advanced 3D visualizations.

The complete code for this episode is available in the `code/episode_7` directory. This code defines a Trame application that presents three views (one each for Plotly, PyVista, and VTK) that the user can choose between with a tab widget.

## Setup

Let\'s start by setting up a new application from the template.

```bash
copier copy https://code.ornl.gov/ndip/project-templates/nova-application-template.git viz_tutorial
cd viz_tutorial
poetry install
poetry run app
```

Since we\'ve already discussed the data bindings, we will gloss over the data bindings and tab setup. Please copy the following files into your template.

**1. Main View Model (`src/nova_tutorial/view_models/main.py`):**

```python
"""View model for visualization examples."""

from typing import Any, Optional

from nova.mvvm.interface import BindingInterface
from pydantic import BaseModel, Field
from pyvista import Plotter

from nova_tutorial.models.plotly import PlotlyConfig
from nova_tutorial.models.pyvista import PyVistaConfig
from nova_tutorial.models.vtk import VTKConfig


class Controls(BaseModel):
    """General controls for the GUI."""

    active_tab: int = Field(default=0)


class VisualizationViewModel:
    """View model for visualization examples."""

    def __init__(self, binding: BindingInterface):
        self.controls = Controls()
        self.plotly_config = PlotlyConfig()
        self.pyvista_config = PyVistaConfig()
        self.vtk_config = VTKConfig()

        self.controls_bind = binding.new_bind(self.controls)
        self.plotly_config_bind = binding.new_bind(
            linked_object=self.plotly_config, callback_after_update=self.update_plotly_figure
        )
        self.plotly_figure_bind = binding.new_bind()
        self.pyvista_config_bind = binding.new_bind(linked_object=self.pyvista_config)
        self.vtk_config_bind = binding.new_bind(linked_object=self.vtk_config)
        self.render_vtk_bind = binding.new_bind()

    def init_view(self) -> None:
        self.update_plotly_figure()
        self.init_vtk()

    def init_vtk(self) -> None:
        self.render_vtk_bind.update_in_view(self.vtk_config.get_volume())

    def render_pyvista(self, plotter: Plotter) -> None:
        self.pyvista_config.render(plotter)

    def update_plotly_figure(self, _: Optional[dict[str, Any]] = None) -> None:
        self.plotly_config_bind.update_in_view(self.plotly_config)
        self.plotly_figure_bind.update_in_view(self.plotly_config.get_figure())
```

**2. Main View (`src/nova_tutorial/views/main.py`):**

```python
"""View for the visualization examples."""

from typing import Any

from nova.mvvm.trame_binding import TrameBinding
from nova.trame import ThemedApp
from trame.app import get_server
from trame.widgets import vuetify3 as vuetify

from nova_tutorial.view_models.main import VisualizationViewModel
from nova_tutorial.views.plotly import PlotlyView
from nova_tutorial.views.pyvista import PyVistaView
from nova_tutorial.views.vtk import VTKView


class VisualizationApp(ThemedApp):  # Inherits from nova.trame.ThemedApp for consistent styling
    """View class for the visualization examples."""

    def __init__(self) -> None:
        super().__init__()
        self.server = get_server(None, client_type="vue3")
        self.ctrl = self.server.controller

        self.view_model = VisualizationViewModel(TrameBinding(self.server.state))
        self.view_model.controls_bind.connect("controls")

        self.create_ui()

        # This makes the loading of the initial Trame state asynchronous, which is useful for improving the launch time
        # of the application.
        self.ctrl.on_server_ready.add(self.server_ready)

    def server_ready(self, **_kwargs: Any) -> None:
        self.view_model.init_view()

    def create_ui(self) -> None:
        self.state.trame__title = "NOVA Tutorial"
        with super().create_ui() as layout:
            with layout.pre_content:
                with vuetify.VTabs(
                    v_model="controls.active_tab", classes="pl-4", update_modelValue="flushState('controls');"
                ):
                    vuetify.VTab("Plotly", value=0)
                    vuetify.VTab("PyVista", value=1)
                    vuetify.VTab("VTK", value=2)

            with layout.content:
                with vuetify.VCard():
                    with vuetify.VTabsWindow(v_model="controls.active_tab"):
                        with vuetify.VTabsWindowItem(value=0):
                            PlotlyView(self.view_model)
                        with vuetify.VTabsWindowItem(value=1):
                            PyVistaView(self.view_model)
                        with vuetify.VTabsWindowItem(value=2):
                            VTKView(self.view_model)

            layout.post_content.classes += "mb-4"

            return layout
```

We\'ll also need to stub out each of the classes we\'ll build so that the application can be run after each step.

**3. `PlotlyView` (`src/nova_tutorial/views/plotly.py`):**

```python
class PlotlyView:
    pass
```

**4. `PlotlyConfig` (`src/nova_tutorial/models/plotly.py`):**

```python
class PlotlyConfig:
    pass
```

**5. `PyVistaView` (`src/nova_tutorial/views/pyvista.py`):**

```python
class PyVistaView:
    pass
```

**6. `PyVistaConfig` (`src/nova_tutorial/models/pyvista.py`):**

```python
class PyVistaConfig:
    pass
```

**7. `VTKView` (`src/nova_tutorial/views/vtk.py`):**

```python
class VTKView:
    pass
```

**8. `VTKConfig` (`src/nova_tutorial/models/vtk.py`):**

```python
class VTKConfig:
    pass
```

## Plotly (2D)

Trame provides a library called [trame-plotly](https://github.com/Kitware/trame-plotly) for connecting Trame and [Plotly](https://plotly.com/python/). You can install it with:

```bash
poetry add plotly trame-plotly
```

Now, we can create a view that displays a Plotly figure.

**9. `PlotlyView` View Class (`src/nova_tutorial/views/plotly.py`):**

*   **Imports**:  Pay special attention to the plotly import. This module contains a Trame widget that will allow us to quickly add a Plotly chart to our view.

    ```python
    """View for Plotly."""

    import plotly.graph_objects as go
    from nova.trame.view.components import InputField
    from nova.trame.view.layouts import GridLayout, HBoxLayout
    from trame.widgets import plotly

    from nova_tutorial.view_models.visualization import VisualizationViewModel
    ```

*   **Class Definition**:  The view model connections allow us to connect the controls we will define in create_ui() to the server and update the Plotly chart after a control is changed.

    ```python
    class PlotlyView:
        """View class for Plotly."""

        def __init__(self, view_model: VisualizationViewModel) -> None:
            self.view_model = view_model
            self.view_model.plotly_config_bind.connect("plotly_config")
            self.view_model.plotly_figure_bind.connect(self.update_figure)

            self.create_ui()
    ```

*   **Controls**:  These controls will dynamically update the Plotly chart.

    ```python
        def create_ui(self) -> None:
            with GridLayout(columns=4, classes="mb-2"):
                InputField(v_model="plotly_config.plot_type", items="plotly_config.plot_type_options", type="select")
                InputField(v_model="plotly_config.x_axis", items="plotly_config.axis_options", type="select")
                InputField(v_model="plotly_config.y_axis", items="plotly_config.axis_options", type="select")
                InputField(
                    v_model="plotly_config.z_axis",
                    disabled=("plotly_config.is_not_heatmap",),
                    items="plotly_config.axis_options",
                    type="select",
                )
    ```

*   **Chart Definition**:  Here, we use the imported Trame widget for Plotly to define the chart. This widget includes an `update` method that allows us to change the content after the initial rendering.

    ```python
            with HBoxLayout(halign="center", height="50vh"):
                self.figure = plotly.Figure()

        def update_figure(self, figure: go.Figure) -> None:
            self.figure.update(figure)
            self.figure.state.flush()  # This is necessary if you call update asynchronously.
    ```

As with our previous examples, there is a corresponding model.

**10. `PlotlyConfig` Model Class (src/nova_tutorial/models/plotly.py):**

*   **Imports**:  The graph_objects module is how we will define the content for our chart. The iris module defines an example dataset.

    ```python
    """Configuration for the Plotly example."""

    import plotly.graph_objects as go
    from plotly.data import iris
    from pydantic import BaseModel, Field, computed_field

    IRIS_DATA = iris()
    ```

*   **Pydantic definition**:  Here we define the controls for our view.

    ```python
    class PlotlyConfig(BaseModel):
        """Configuration class for the Plotly example."""

        axis_options: list[str] = ["sepal_length", "sepal_width", "petal_length", "petal_width"]
        x_axis: str = Field(default="sepal_length", title="X Axis")
        y_axis: str = Field(default="sepal_width", title="Y Axis")
        z_axis: str = Field(default="petal_length", title="Color")
        plot_type: str = Field(default="scatter", title="Plot Type")
        plot_type_options: list[str] = ["heatmap", "scatter"]

        @computed_field  # type: ignore
        @property
        def is_not_heatmap(self) -> bool:
            return self.plot_type != "heatmap"
    ```

*   **Plotly Figure Setup**:  Finally, we define the Plotly figure based on the user\'s selection. go.Heatmap and go.Scatter define Plotly `traces`, which represent individual components of the figure.

    ```python
        def get_figure(self) -> go.Figure:
            match self.plot_type:
                case "heatmap":
                    plot_data = go.Heatmap(x=IRIS_DATA[self.x_axis], y=IRIS_DATA[self.y_axis], z=IRIS_DATA[self.z_axis])
                case "scatter":
                    plot_data = go.Scatter(x=IRIS_DATA[self.x_axis], y=IRIS_DATA[self.y_axis], mode="markers")
                case _:
                    raise ValueError(f"Invalid plot type: {self.plot_type}")

            figure = go.Figure(plot_data)
            figure.update_layout(
                title={"text": f"{self.plot_type}"},
                xaxis={"title": {"text": self.x_axis}},
                yaxis={"title": {"text": self.y_axis}},
            )

            return figure
    ```

Now, if you run the application you should see the following in the Plotly tab:

![Plotly chart](fig/plotly.png)

## PyVista (3D)

One of Trame\'s core features is that it has direct integration with VTK for building 3D visualizations. Learning VTK from scratch is non-trivial, however, so we recommend that you work with PyVista. PyVista serves as a more developer-friendly wrapper around VTK, allowing you to build your visualizations with a simpler, more intuitive API. To get started, you will need to install the Python package.

```bash
poetry add pyvista trame-vtk
```

PyVista contains built-in Trame support, but we still need to install the Trame widget for VTK that PyVista will use internally.

Now we can set up our view.

**11. `PyVistaView` View Class (`src/nova_tutorial/views/pyvista.py`):**

*   **Imports:**  `plotter_ui` contains the Trame widget for PyVista.

    ```python
    """View for the 3d plot using PyVista."""

    from typing import Any, Optional

    import pyvista as pv
    from nova.trame.view.components import InputField
    from nova.trame.view.layouts import GridLayout, HBoxLayout
    from pyvista.trame.ui import plotter_ui
    from trame.widgets import vuetify3 as vuetify

    from nova_tutorial.view_models.visualization import VisualizationViewModel
    ```

*   **Class Definition:**  The `Plotter` object is PyVista\'s main entry point. It will allow you to add meshes and volumes with the properties you\'ve specified.

    ```python
    class PyVistaView:
        """View class for the 3d plot using PyVista."""

        def __init__(self, view_model: VisualizationViewModel) -> None:
            self.view_model = view_model
            self.view_model.pyvista_config_bind.connect("pyvista_config")

            self.plotter: Optional[pv.Plotter] = None

            self.create_plotter()
            self.create_ui()

        def create_plotter(self) -> None:
            self.plotter = pv.Plotter(off_screen=True)
    ```

*   **View Definition:**  Now, we can use `plotter_ui` to create a view into which our rendering will go.

    ```python
        def create_ui(self) -> None:
            vuetify.VCardTitle("PyVista")
            with GridLayout(columns=5, classes="mb-2", valign="center"):
                InputField(
                    v_model="pyvista_config.colormap", column_span=2, items="pyvista_config.colormap_options", type="select"
                )
                InputField(
                    v_model="pyvista_config.opacity", column_span=2, items="pyvista_config.opacity_options", type="select"
                )
                vuetify.VBtn("Render", click=self.update)
            with HBoxLayout(halign="center", height="50vh"):
                plotter_ui(self.plotter)

        def update(self, _: Any = None) -> None:
            if self.plotter:
                self.view_model.render_pyvista(self.plotter)
    ```

**12. `PyVistaConfig` Model Class (`src/nova_tutorial/models/pyvista.py`):**

*   **Imports:**  `download_knee_full` yields a 3D dataset that is suitable for volume rendering. You can find more datasets in PyVista\'s [Dataset Gallery](https://docs.pyvista.org/api/examples/dataset_gallery).

    ```python
    """Configuration for the PyVista example."""

    from pydantic import BaseModel, Field
    from pyvista import Plotter, examples

    KNEE_DATA = examples.download_knee_full()
    ```

*   **Pydantic Configuration:**  The `Fields` defined here will be passed to [`Plotter.add_volume`](https://docs.pyvista.org/api/plotting/_autosummary/pyvista.plotter.add_volume).

    ```python
    class PyVistaConfig(BaseModel):
        """Configuration class for the PyVista example."""

        colormap_options: list[str] = ["viridis", "autumn", "coolwarm", "twilight", "jet"]
        opacity_options: list[str] = ["linear", "sigmoid"]
        colormap: str = Field(default="viridis", title="Color Transfer Function")
        opacity: str = Field(default="linear", title="Opacity Transfer Function")
    ```

*   **Rendering:**  `add_volume` will return an actor. In practice, you may get better performance by manipulating that actor instead of doing a full re-render.

    ```python
        def render(self, plotter: Plotter) -> None:
            # If re-rendering the volume on changes isn't acceptable, then you may need to switch to using VTK directly due
            # limitations of the PyVista volume rendering engine.
            plotter.clear()
            plotter.add_volume(KNEE_DATA, cmap=self.colormap, opacity=self.opacity, show_scalar_bar=False)

            plotter.render()
            plotter.view_isometric()
    ```

::::::::::::::::::::::::::: callout

PyVista\'s volume rendering engine isn\'t currently suitable for large data. If you find yourself running into performance issues, then you should likely switch over to using VTK directly.

:::::::::::::::::::::::::::::::::::

Now, if you run the application you should see the following in the PyVista tab:

![PyVista chart](fig/pyvista.png)

## VTK (3D)

If you have prior experience with VTK then you may prefer to work with it directly. You can get started with it by installing the Python VTK bindings and the Trame widget for VTK.

```bash
poetry add trame-vtk vtk
```

Since we\'ve seen plenty of examples of UI controls at this point, we\'ve omitted them for this example so that we can focus on the VTK boilerplate needed to get started.

**13. `VTKView` View Class (`src/nova_tutorial/views/vtk.py`):**

*   **Imports:**  The `vtkRenderingVolumeOpenGL2` import is necessary despite being unreferenced.

    ```python
    """View for the 3d plot using PyVista."""

    import vtkmodules.vtkRenderingVolumeOpenGL2  # noqa
    from nova.trame.view.layouts import HBoxLayout
    from trame.widgets import vtk as vtkw
    from trame.widgets import vuetify3 as vuetify
    from vtkmodules.vtkRenderingCore import vtkRenderer, vtkRenderWindow, vtkRenderWindowInteractor, vtkVolume

    from nova_tutorial.view_models.visualization import VisualizationViewModel
    ```

*   **Initialization:**  Here we define the boiler plate for the interactive VTK window. As with PyVista, setting off-screen rendering to on is necessary when working with Trame.

    ```python
    class VTKView:
        """View class for the 3d plot using PyVista."""

        def __init__(self, view_model: VisualizationViewModel) -> None:
            self.view_model = view_model
            self.view_model.render_vtk_bind.connect(self.render)

            self.create_vtk()
            self.create_ui()

        def create_vtk(self) -> None:
            self.renderer = vtkRenderer()
            self.renderer.SetBackground(0.7, 0.7, 0.7)

            self.render_window = vtkRenderWindow()
            self.render_window.AddRenderer(self.renderer)
            self.render_window.OffScreenRenderingOn()

            self.render_window_interactor = vtkRenderWindowInteractor()
            self.render_window_interactor.SetRenderWindow(self.render_window)
            self.render_window_interactor.GetInteractorStyle().SetCurrentStyleToTrackballCamera()
            self.render_window_interactor.Initialize()  # Ensure interactor is initialized
    ```

*   **View Definition:**  Now, we setup the VTK window and add our volume rendering to it. By using `VTKRemoteView`, we are instructing VTK to perform server-side rendering.

    ```python
        def create_ui(self) -> None:
            vuetify.VCardTitle("VTK")

            with HBoxLayout(halign="center", height="50vh"):
                self.view = vtkw.VtkRemoteView(self.render_window, interactive_ratio=1)

        def render(self, volume: vtkVolume) -> None:
            self.renderer.Clear()
            self.renderer.AddVolume(volume)
            self.render_window.Render()
    ```

**14. `VTKConfig` Model Class (`src/nova_tutorial/models/vtk.py`):**

*   **Imports:**  We are only using PyVista to get an example dataset. There are two references to it as we use `KNEE_DATA` to compute min/max bounds for the data and `KNEE_DATAFILE` to pass the data file into a VTK reader. The FixedPointVolumeRayCastMapper is CPU-based, but other mappers are available if you need GPU support.

    ```python
    """Configuration for the VTK example."""

    import numpy as np
    from pyvista import examples
    from vtk import vtkSLCReader
    from vtkmodules.vtkCommonDataModel import vtkPiecewiseFunction
    from vtkmodules.vtkRenderingCore import vtkColorTransferFunction, vtkVolume, vtkVolumeProperty
    from vtkmodules.vtkRenderingVolume import vtkFixedPointVolumeRayCastMapper

    KNEE_DATA = examples.download_knee_full()
    KNEE_DATAFILE = examples.download_knee_full(load=False)
    ```

*   **VTK Pipeline Setup:**  The dataset is stored in .slc format, so we can use a built-in VTK reader to load it into a pipeline. From there, we setup the volume. A lookup table is used to define the color transfer function, and a piecewise function is used to define the opacity transfer function.

    ```python
    class VTKConfig:
        """Configuration class for the VTK example."""

        max: float = KNEE_DATA.get_data_range()[1]
        min: float = KNEE_DATA.get_data_range()[0]

        def __init__(self) -> None:
            reader = vtkSLCReader()
            reader.SetFileName(KNEE_DATAFILE)

            mapper = vtkFixedPointVolumeRayCastMapper()
            mapper.SetInputConnection(reader.GetOutputPort())

            lut = self.init_lut()
            pwf = self.init_pwf()
            volume_props = vtkVolumeProperty()
            volume_props.SetColor(lut)
            volume_props.SetScalarOpacity(pwf)
            volume_props.SetShade(0)
            volume_props.SetInterpolationTypeToLinear()

            self.volume = vtkVolume()
            self.volume.SetMapper(mapper)
            self.volume.SetProperty(volume_props)
            self.volume.SetVisibility(1)

        def get_volume(self) -> vtkVolume:
            return self.volume
    ```

Now, if you run the application you should see the following in the VTK tab:

![VTK chart](fig/vtk.png)

:::::::::::::::::::::::::::::::::::::::  challenge
**Plotly Box Plot**
Add a box plot to the available plot types. Hint: you shouldn\'t need to change anything in the view class to do this.
::::::::::::::::::::::::::::::::::::::::::::::::::

:::::::::::::::::::::::::::::::::::::::  challenge
**PyVista clim Control**
Add control(s) to the UI to control the `clim` argument for the `add_volume` method.
::::::::::::::::::::::::::::::::::::::::::::::::::

:::::::::::::::::::::::::::::::::::::::  challenge
**Investigate the lookup table and piecewise function**
We didn\'t look at `VTKConfig.init_lut` or `VTKConfig.init_pwf` during the tutorial. Read through these methods and then trys manipulating the opacity of the rendering.
::::::::::::::::::::::::::::::::::::::::::::::::::

## References

*   **Plotly Documentation**: https://plotly.com/python/
*   **Trame/Plotly Integration Repository**: https://github.com/Kitware/trame-plotly
*   **PyVista Documentation**: https://docs.pyvista.org/
*   **Trame/PyVista Integration Tutorial**: https://tutorial.pyvista.org/tutorial/09_trame/index.html
*   **VTK Python Documentation**: https://docs.vtk.org/en/latest/api/python.html
*   **Trame Tutorial**: https://kitware.github.io/trame/guide/tutorial/

:::::::::::::::::::::::::::::::::::::::: keypoints
- Trame integrates well with Plotly for building 2D charts.
- Trame integrates well with PyVista and VTK for building 3D visualizations.
- PyVista provides a simpler API compared to VTK at the cost of performance.
::::::::::::::::::::::::::::::::::::::::::::::::::
