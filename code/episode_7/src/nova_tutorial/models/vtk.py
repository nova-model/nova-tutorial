"""Configuration for the VTK example."""

import numpy as np
from pyvista import examples
from vtk import vtkSLCReader
from vtkmodules.vtkCommonDataModel import vtkPiecewiseFunction
from vtkmodules.vtkRenderingCore import vtkColorTransferFunction, vtkVolume, vtkVolumeProperty
from vtkmodules.vtkRenderingVolume import vtkFixedPointVolumeRayCastMapper

KNEE_DATA = examples.download_knee_full()
KNEE_DATAFILE = examples.download_knee_full(load=False)


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

    def init_lut(self) -> vtkColorTransferFunction:
        # This method defines the "Fast" colormap.
        # See https://www.kitware.com/new-default-colormap-and-background-in-next-paraview-release/

        lut = vtkColorTransferFunction()

        lut.SetColorSpaceToRGB()
        lut.SetNanColor([0.0, 1.0, 0.0])

        srgb = np.array(
            [
                0,
                0.05639999999999999,
                0.05639999999999999,
                0.47,
                0.17159223942480895,
                0.24300000000000013,
                0.4603500000000004,
                0.81,
                0.2984914818394138,
                0.3568143826543521,
                0.7450246485363142,
                0.954367702893722,
                0.4321287371255907,
                0.6882,
                0.93,
                0.9179099999999999,
                0.5,
                0.8994959551205902,
                0.944646394975174,
                0.7686567142818399,
                0.5882260353170073,
                0.957107977357604,
                0.8338185108985666,
                0.5089156299842102,
                0.7061412605695164,
                0.9275207599610714,
                0.6214389091739178,
                0.31535705838676426,
                0.8476395308725272,
                0.8,
                0.3520000000000001,
                0.15999999999999998,
                1,
                0.59,
                0.07670000000000013,
                0.11947499999999994,
            ]
        )

        for arr in np.split(srgb, len(srgb) / 4):
            lut.AddRGBPoint(arr[0], arr[1], arr[2], arr[3])

        prev_min, prev_max = lut.GetRange()
        prev_delta = prev_max - prev_min
        node = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        next_delta = self.max - self.min
        for i in range(lut.GetSize()):
            lut.GetNodeValue(i, node)
            node[0] = next_delta * (node[0] - prev_min) / prev_delta + self.min
            lut.SetNodeValue(i, node)

        return lut

    def init_pwf(self) -> vtkPiecewiseFunction:
        pwf = vtkPiecewiseFunction()

        pwf.RemoveAllPoints()
        pwf.AddPoint(self.min, 0)
        pwf.AddPoint(self.max, 0.7)

        return pwf
