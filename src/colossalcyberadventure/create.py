import json

MAP_WIDTH_PX = 2400
MAP_HEIGHT_PX = 1350

with open("resources/map/example.tmx", "r") as ex:
    text = ex.read()


def create_file(name):
    with open(f"resources/map/{name}.tmx", "w") as f:
        f.write(text)


j = {"maps": []}
for y in range(30):
    for x in range(30):
        j["maps"].append({"fileName": f"{x}-{y}.tmx", "height": 1440, "width": 2560, "x": y * 2560, "y": -x * 1440})
        create_file(f"{x}-{y}")

world = open("resources/map/map.world", "w")
json.dump(j, world, indent=4)
world.close()
