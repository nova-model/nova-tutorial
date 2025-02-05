import importlib.metadata

from .main import main

__all__ = ["main"]

__version__ = importlib.metadata.version(__package__)
