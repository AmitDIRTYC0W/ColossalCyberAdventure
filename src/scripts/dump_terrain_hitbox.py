import json

import arcade

scene = arcade.Scene.from_tilemap(arcade.load_tilemap("../colossalcyberadventure/resources/map/0-0.tmx", layer_options={
    "Trees": {
        "use_spatial_hash": True,
    }
}))

# with open("static_hitboxes.txt", "w") as f:
# for sprite in scene.name_mapping["Trees"]:
# f.write(str(sprite.get_adjusted_hit_box()) + "\n")

hitboxes = {"Trees": []}

for sprite in scene.name_mapping["Trees"]:
    hitboxes["Trees"].append(str(sprite.get_adjusted_hit_box()))

with open("static_hitboxes.json", "w") as f:
    json.dump(hitboxes, f, indent=4)
