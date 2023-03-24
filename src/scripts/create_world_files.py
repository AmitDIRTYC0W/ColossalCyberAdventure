import json
import random

MAP_WIDTH_PX = 1920
MAP_HEIGHT_PX = 1080

texts = []
for i in range(6):
    with open(f"example{i}.tmx", "r") as ex:
        texts.append(ex.read())


def create_file(name):
    with open(f":data:map/{name}.tmx", "w") as f:
        f.write(texts[random.randint(0, 5)])


j = {"maps": []}
for y in range(40):
    for x in range(40):
        j["maps"].append({"fileName": f"{x}-{y}.tmx", "height": 544, "width": 960, "x": y * 960, "y": -x * 544})
        create_file(f"{x}-{y}")

world = open(":data:map/map.world", "w")
json.dump(j, world, indent=4)
world.close()
