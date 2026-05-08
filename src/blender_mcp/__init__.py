"""Blender integration through the Model Context Protocol."""

__version__ = "0.1.0"

# Expose key classes and functions for easier imports
from .server import (
    BlenderConnection as BlenderConnection,
    get_blender_connection as get_blender_connection,
)
