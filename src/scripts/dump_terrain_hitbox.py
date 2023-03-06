import json

import arcade

scene = arcade.Scene.from_tilemap(arcade.load_tilemap("../colossalcyberadventure/resources/map/0-0.tmx", layer_options={
    "Trees": {
        "use_spatial_hash": True,
    }
}))

hitboxes = {"Trees": []}

for i, sprite in enumerate(scene.name_mapping["Trees"]):
    hitboxes["Trees"].append([])
    for x, y in sprite.get_adjusted_hit_box():
        hitboxes["Trees"][i].append((x, y))

with open("static_hitboxes.json", "w") as f:
    json.dump(hitboxes, f, indent=4)
