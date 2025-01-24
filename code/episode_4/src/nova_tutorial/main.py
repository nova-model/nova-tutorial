"""Main Application."""

from nova.mvvm.trame_binding import TrameBinding
from nova_tutorial.view_models.fractal_view_model import FractalViewModel
from trame.app import get_server

def main():
    server = get_server(None, client_type="vue3")
    binding = TrameBinding(server.state)
    fractal_vm = FractalViewModel(binding)
    try:
        fractal_vm.run_fractal_tool()
    except Exception as e:
        print(f"Error running fractal tool: {e}")


if __name__ == "__main__":
    main()