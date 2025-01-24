"""Main Application."""

from nova_tutorial.view_models.fractal_view_model import FractalViewModel

def main():
    fractal_vm = FractalViewModel()
    try:
        fractal_vm.run_fractal_tool()
    except Exception as e:
        print(f"Error running fractal tool: {e}")

if __name__ == "__main__":
    main()