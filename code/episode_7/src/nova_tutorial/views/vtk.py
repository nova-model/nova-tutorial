"""View for the 3d plot using PyVista."""

import vtkmodules.vtkRenderingVolumeOpenGL2  # noqa
from nova.trame.view.layouts import HBoxLayout
from trame.widgets import vtk as vtkw
from trame.widgets import vuetify3 as vuetify
from vtkmodules.vtkRenderingCore import vtkRenderer, vtkRenderWindow, vtkRenderWindowInteractor, vtkVolume

from nova_tutorial.view_models.main import VisualizationViewModel


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

    def create_ui(self) -> None:
        vuetify.VCardTitle("VTK")

        with HBoxLayout(halign="center", height="50vh"):
            self.view = vtkw.VtkRemoteView(self.render_window, interactive_ratio=1)

    def render(self, volume: vtkVolume) -> None:
        self.renderer.Clear()
        self.renderer.AddVolume(volume)
        self.render_window.Render()
