"""Module for the main model."""

from pydantic import BaseModel, Field
from .fractal import Fractal


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
    file: str = Field(default="", title="Select a File")
