"""Test package for application."""

from trame_with_pydantic.app.views.main import MainApp


def test_app() -> None:
    app = MainApp()
    assert app
