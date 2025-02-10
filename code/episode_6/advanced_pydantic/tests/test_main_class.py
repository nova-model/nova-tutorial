"""Test package."""

from advanced_pydantic import MainClass


def test_version() -> None:
    app = MainClass()
    assert app.name("test") == "test"
