"""Main Application."""

from typing import List, Literal

from pydantic import BaseModel, Field, ValidationError, field_validator, model_validator
from typing_extensions import Self


class Address(BaseModel):
    """User Address model."""

    street: str = Field(min_length=3, max_length=50)
    city: str = Field(min_length=2, max_length=30)
    zip_code: str = Field(pattern=r"^\d{5}$")  # US ZIP code validation
    type: Literal["home", "work"] = Field()


class User(BaseModel):
    """User model."""

    id: int = Field(default=1, gt=0)
    name: str = Field(default="someName", min_length=1)
    addresses: List[Address] = Field(min_length=1)

    @field_validator("id", mode="after")
    @classmethod
    def is_even(cls, value: int) -> int:
        if value % 2 == 1:
            raise ValueError(f"{value} is not an even number")
        return value

    @model_validator(mode="after")
    def check_name_for_even_id(self) -> Self:
        if self.id % 2 == 0 and not self.name[0].isupper():
            raise ValueError("Name must start with a capital letter when the ID is even.")

        return self


def main() -> None:
    # Example input
    user_data = {
        "id": 2,
        "name": "Alice",
        "addresses": [{"street": "123 Main St", "city": "New York", "zip_code": "10001", "type": "home"}],
    }

    try:
        user = User.model_validate(user_data)
        print(user)
    except ValidationError as e:
        print(e)
