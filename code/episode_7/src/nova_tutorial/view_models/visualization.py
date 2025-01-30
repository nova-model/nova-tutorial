"""View model for visualization examples."""

from typing import Any, Optional

from nova.mvvm.interface import BindingInterface  # type: ignore
from pydantic import BaseModel, Field
from pyvista import Plotter

from nova_tutorial.models.plotly import PlotlyConfig
from nova_tutorial.models.pyvista import PyVistaConfig
from nova_tutorial.models.vtk import VTKConfig


class Controls(BaseModel):
    """General controls for the GUI."""

    active_tab: int = Field(default=1)


class VisualizationViewModel:
    """View model for visualization examples."""

    def __init__(self, binding: BindingInterface):
        self.controls = Controls()
        self.config_2d = PlotlyConfig()
        self.config_pyvista = PyVistaConfig()
        self.config_vtk = VTKConfig()

        self.controls_bind = binding.new_bind()
        self.config_2d_bind = binding.new_bind(linked_object=self.config_2d, callback_after_update=self.update_2d_plot)
        self.config_pyvista_bind = binding.new_bind(
            linked_object=self.config_pyvista, callback_after_update=self.update_pyvista
        )
        self.config_vtk_bind = binding.new_bind()

    def init_view(self) -> None:
        self.controls_bind.update_in_view(self.controls)
        self.update_2d_plot()
        self.update_pyvista()
        self.update_vtk()

    def update_2d_plot(self, results: Optional[dict[str, Any]] = None) -> None:
        self.config_2d.update()
        self.config_2d_bind.update_in_view(self.config_2d)

    def update_pyvista(self, results: Optional[dict[str, Any]] = None) -> None:
        self.config_pyvista_bind.update_in_view(self.config_pyvista)

    def render_pyvista(self, plotter: Optional[Plotter]) -> None:
        self.config_pyvista.update(plotter)

    def update_vtk(self) -> None:
        self.config_vtk_bind.update_in_view(self.config_vtk.get_volume())
