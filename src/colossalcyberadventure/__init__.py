from pathlib import Path
import arcade

__version__ = '0.1.0'

# Add a handle for game resources: data:bullet/0.png
RESOURCE_ROOT = Path(__file__).parent / "resources"
arcade.resources.add_resource_handle("data", RESOURCE_ROOT)
