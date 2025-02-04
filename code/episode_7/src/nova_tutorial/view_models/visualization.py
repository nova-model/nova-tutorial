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
