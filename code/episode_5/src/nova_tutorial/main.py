from nova_tutorial.views.fractal_view import FractalApp

def main():
    app = FractalApp()
    app.server.start()

if __name__ == "__main__":
    main()