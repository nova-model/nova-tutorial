"""Configuration for the Plotly example."""

from typing import Any

from plotly.data import iris  # type: ignore
from pydantic import BaseModel, Field, computed_field

IRIS_DATA = iris()


class PlotlyConfig(BaseModel):
    """Configuration class for the Plotly example."""

    axis_options: list[str] = ["sepal_length", "sepal_width", "petal_length", "petal_width", "species", "species_id"]
    x_axis: str = Field(default="sepal_length", title="X Axis")
    y_axis: str = Field(default="sepal_width", title="Y Axis")
    z_axis: str = Field(default="petal_length", title="Z Axis")
    plot_data: Any = None
    plot_type: str = Field(default="scatter", title="Plot Type")
    plot_type_options: list[str] = ["heatmap", "scatter"]

    @computed_field  # type: ignore
    @property
    def is_scatter(self) -> bool:
        return self.plot_type == "scatter"

    def update(self) -> None:
        self.plot_data = {
            "data": [
                {
                    "x": IRIS_DATA[self.x_axis].tolist(),
                    "y": IRIS_DATA[self.y_axis].tolist(),
                    "z": IRIS_DATA[self.z_axis].tolist(),
                    "type": self.plot_type,
                    "mode": "markers",
                    "colorbar": {"title": self.z_axis},
                    "colorscale": "Viridis",
                }
            ],
            "layout": {
                "title": "Iris Flower Data Set",
                "xaxis": {"fixedrange": True, "title": self.x_axis},
                "yaxis": {"fixedrange": True, "title": self.y_axis},
            },
        }
