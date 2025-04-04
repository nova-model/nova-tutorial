"""Configuration for the PyVista example."""

from enum import Enum

from pydantic import BaseModel, Field
from pyvista import Plotter, examples

KNEE_DATA = examples.download_knee_full()

class ColormapOptions(str, Enum):
    viridis = "viridis"
    autumn = "autumn"
    coolwarm = "coolwarm"
    twilight = "twilight"
    jet = "jet"


class OpacityOptions(str, Enum):
    linear = "linear"
    sigmoid = "sigmoid"


class PyVistaConfig(BaseModel):
    """Configuration class for the PyVista example."""

    colormap: ColormapOptions = Field(default=ColormapOptions.viridis, title="Color Transfer Function")
    opacity: OpacityOptions = Field(default=OpacityOptions.linear, title="Opacity Transfer Function")

    def render(self, plotter: Plotter) -> None:
        # If re-rendering the volume on changes isn't acceptable, then you may need to switch to using VTK directly due
        # limitations of the PyVista volume rendering engine.
        plotter.clear()
        plotter.add_volume(KNEE_DATA, cmap=self.colormap, opacity=self.opacity, show_scalar_bar=False)

        plotter.render()
        plotter.view_isometric()
