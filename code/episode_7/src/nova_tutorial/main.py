"""Loads the main view and starts the Trame server."""

from nova_tutorial.views.main import MainApp


def main() -> None:
    app = MainApp()
    app.server.start()


if __name__ == "__main__":
    main()
