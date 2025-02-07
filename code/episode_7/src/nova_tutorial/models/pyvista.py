"""Configuration for the PyVista example."""

from pydantic import BaseModel, Field
from pyvista import Plotter, examples

KNEE_DATA = examples.download_knee_full()


class PyVistaConfig(BaseModel):
    """Configuration class for the PyVista example."""

    colormap_options: list[str] = ["viridis", "autumn", "coolwarm", "twilight", "jet"]
    opacity_options: list[str] = ["linear", "sigmoid"]
    colormap: str = Field(default="viridis", title="Color Transfer Function")
    opacity: str = Field(default="linear", title="Opacity Transfer Function")

    def render(self, plotter: Plotter) -> None:
        # If re-rendering the volume on changes isn't acceptable, then you may need to switch to using VTK directly due
        # limitations of the PyVista volume rendering engine.
        plotter.clear()
        plotter.add_volume(KNEE_DATA, cmap=self.colormap, opacity=self.opacity, show_scalar_bar=False)

        plotter.render()
        plotter.view_isometric()
