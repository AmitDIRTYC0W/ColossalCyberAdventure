import multiprocessing as mp
import arcade
from pytiled_parser import World
from colossalcyberadventure import constants
from pyglet.math import Vec2

_LOADER = None


def get_loader():
    """Get the global tilemap loader process"""
    if _LOADER is None:
        raise RuntimeError("Loader not initialized")
    return _LOADER


def init_loader():
    """
    Start the tilemap loader process.
    There should only be one loader process
    """
    global _LOADER
    if _LOADER is not None:
        raise RuntimeError("Loader already initialized")
    _LOADER = TilemapLoader()
    _LOADER.start()


class TilemapLoader:
    def __init__(self):
        self.queue_in = mp.Queue()
        self.queue_out = mp.Queue()
        self.process = mp.Process(
            target=self.load_maps,
            args=(self.queue_in, self.queue_out,),
            daemon=True,
        )

    def load_maps(self, queue_in: mp.Queue, queue_out: mp.Queue):
        command_count = 0
        while True:
            command = queue_in.get(block=True)
            print(
                f"TilemapLoader: command[{command_count}]: {command}",
                # f"size={command.__sizeof__()} type={type(command)}",
            )
            # Handle string commands
            if isinstance(command, str):
                if command == "start":
                    queue_out.put("started", block=True)

            # Handle dict commands (loading tilemaps)
            elif isinstance(command, dict):
                params = command
                map_loaded = tilemap_from_world(
                    params["x"],
                    params["y"],
                    params["map_file"],
                    params["width_px"],
                    params["height_px"],
                )
                queue_out.put(
                    {
                        "tilemap": map_loaded,
                        "x": params["x"],
                        "y": params["y"],
                    },
                    block=False,
                )
            command_count += 1

    def start(self):
        """Start the loader process and wait for the process to start"""
        print("Starting tilemap loader process ..")
        self.process.start()
        self.queue_in.put("start")
        response = self.queue_out.get(block=True)
        if response != "started":
            raise RuntimeError("TilemapLoader did not start")
        print("TilemapLoader started (pid: %d)" % self.process.pid)

    def stop(self):
        self.process.terminate()


def load_tilemap(path: str):
    return arcade.load_tilemap(
        path,
        use_spatial_hash=True,
        lazy=True,
    )


def tilemap_from_world(
    x,
    y,
    map_file,
    tilemap_width_px,
    tilemap_height_px,
):
    return arcade.load_tilemap(
        map_file,
        layer_options={
            "water": {
                "use_spatial_hash": True,
            },
            "obstacles": {
                "use_spatial_hash": True,
            }
        },
        offset=Vec2(x * tilemap_width_px, y * tilemap_height_px),
        scaling=constants.TILE_SCALING,
        lazy=True,
    )
