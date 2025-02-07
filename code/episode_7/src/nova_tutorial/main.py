"""Loads the main view and starts the Trame server."""

from nova_tutorial.views.main import VisualizationApp


def main() -> None:
    app = VisualizationApp()
    app.server.start()


if __name__ == "__main__":
    main()
