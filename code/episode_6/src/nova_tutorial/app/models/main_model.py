"""Module for the main model."""

from pydantic import BaseModel, Field
from .fractal import Fractal
from .sample_tab_models import SampleTab1Model, SampleTab2Model


class MainModel(BaseModel):
    """
    A model class.

    This class uses Pydantic (https://docs.pydantic.dev/latest/),
    which allows for defining data validation rules,
    titles, descriptions, and examples that can be used in GUI elements or
    other interfaces for improved clarity and usability.
    """

    username: str = Field(
        default="test_name",
        min_length=1,
        title="User Name",
        description="Please provide the name of the user",
        examples=["user"],
    )
    password: str = Field(default="test_password", title="User Password")
    fractal: Fractal = Field(default_factory=Fractal)
    sample_tab1: SampleTab1Model = Field(default_factory=SampleTab1Model)
    sample_tab2: SampleTab2Model = Field(default_factory=SampleTab2Model)