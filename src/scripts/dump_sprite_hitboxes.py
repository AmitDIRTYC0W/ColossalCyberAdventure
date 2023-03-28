import json

import arcade

base = "../colossalcyberadventure/resources/"
arcade.resources.add_resource_handle("base", base)

slime_left, slime_right = arcade.load_texture_pair(":base:enemies/slime/idle/0.png")
slime_left, slime_right = arcade.Sprite(slime_left), arcade.Sprite(slime_right)

skeleton_left, skeleton_right = arcade.load_texture_pair(":base:enemies/skeleton/idle/0.png")
skeleton_left, skeleton_right = arcade.Sprite(skeleton_left), arcade.Sprite(skeleton_right)

archer_left, archer_right = arcade.load_texture_pair(":base:enemies/archer/idle/0.png")
archer_left, archer_right = arcade.Sprite(archer_left), arcade.Sprite(archer_right)

player_left, player_right = arcade.load_texture_pair(":base:player/idle/0.png")
player_left, player_right = arcade.Sprite(player_left), arcade.Sprite(player_right)

hitboxes = {
    "slime": {
        "left": slime_left.hit_box.get_adjusted_points(),
        "right": slime_right.hit_box.get_adjusted_points(),
    },
    "skeleton": {
        "left": skeleton_left.hit_box.get_adjusted_points(),
        "right": skeleton_right.hit_box.get_adjusted_points(),
    },
    "archer": {
        "left": archer_left.hit_box.get_adjusted_points(),
        "right": archer_right.hit_box.get_adjusted_points(),
    },
    "player": {
        "left": player_left.hit_box.get_adjusted_points(),
        "right": player_right.hit_box.get_adjusted_points(),
    },
}


with open("hitboxes.json", "w") as f:
    json.dump(hitboxes, f, indent=4)
