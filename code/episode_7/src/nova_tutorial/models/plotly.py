"""Configuration for the Plotly example."""

from enum import Enum

import plotly.graph_objects as go
from plotly.data import iris
from pydantic import BaseModel, Field, computed_field

IRIS_DATA = iris()

class AxisOptions(str, Enum):
    sepal_length = "sepal_length"
    sepal_width = "sepal_width"
    petal_length = "petal_length"
    petal_width = "petal_width"


class PlotTypeOptions(str, Enum):
    heatmap = "Heatmap"
    scatter = "Scatterplot"


class PlotlyConfig(BaseModel):
    """Configuration class for the Plotly example."""

    x_axis: AxisOptions = Field(default=AxisOptions.sepal_length, title="X Axis")
    y_axis: AxisOptions = Field(default=AxisOptions.sepal_width, title="Y Axis")
    z_axis: AxisOptions = Field(default=AxisOptions.petal_length, title="Color")
    plot_type: PlotTypeOptions = Field(default=PlotTypeOptions.scatter, title="Plot Type")

    @computed_field  # type: ignore
    @property
    def is_not_heatmap(self) -> bool:
        return self.plot_type != PlotTypeOptions.heatmap

    def get_figure(self) -> go.Figure:
        match self.plot_type:
            case PlotTypeOptions.heatmap:
                plot_data = go.Heatmap(
                    x=IRIS_DATA[self.x_axis].tolist(),
                    y=IRIS_DATA[self.y_axis].tolist(),
                    z=IRIS_DATA[self.z_axis].tolist(),
                )
            case PlotTypeOptions.scatter:
                plot_data = go.Scatter(
                    x=IRIS_DATA[self.x_axis].tolist(), y=IRIS_DATA[self.y_axis].tolist(), mode="markers"
                )
            case _:
                raise ValueError(f"Invalid plot type: {self.plot_type}")

        figure = go.Figure(plot_data)
        figure.update_layout(
            title={"text": f"{self.plot_type}"},
            xaxis={"title": {"text": self.x_axis}},
            yaxis={"title": {"text": self.y_axis}},
        )

        return figure
