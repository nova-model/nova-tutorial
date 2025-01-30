"""Main Application."""

from nova_tutorial.models.fractal import Fractal

def main():
    fractal = Fractal()
    try:
        fractal.run_fractal_tool()
    except Exception as e:
        print(f"Error running fractal tool: {e}")

if __name__ == "__main__":
    main()