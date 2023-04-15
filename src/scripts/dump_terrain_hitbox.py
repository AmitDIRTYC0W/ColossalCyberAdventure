import json
import os, sys
import arcade


path = "../colossalcyberadventure/resources/map"
dirs = os.listdir(path)

# This would print all the files and directories
dirs = dirs[:-10]

hitboxes = {"obstacles": []}

for file in dirs:
    file_name = "../colossalcyberadventure/resources/map/" + file
    scene = arcade.Scene.from_tilemap(
        arcade.load_tilemap(file_name, layer_options={
            "obstacles": {
                "use_spatial_hash": True,
            }
        }))
    for i, sprite in enumerate(scene.name_mapping["obstacles"]):
        hitboxes["obstacles"].append([])
        for x, y in sprite.get_adjusted_hit_box():
            hitboxes["obstacles"][i].append((x, y))

with open("static_hitboxes.json", "w") as f:
    json.dump(hitboxes, f, indent=4)
