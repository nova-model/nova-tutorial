"""Main Application."""

import sys
from .models.fractal import Fractal


def main() -> None:
    fractal = Fractal()
    try:
        fractal.run_fractal_tool()
    except Exception as e:
        print(f"Error running fractal tool: {e}")

    # kwargs = {}
    # from .views.main_view import MainApp

    # app = MainApp()
    # for arg in sys.argv[2:]:
    #     try:
    #         key, value = arg.split("=")
    #         kwargs[key] = int(value)
    #     except Exception:
    #         pass
    # app.server.start(**kwargs)
