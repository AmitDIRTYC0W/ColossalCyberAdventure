import arcade

from src.colossalcyberadventure.constants import MAP_WIDTH, MAP_HEIGHT


def check_map_bounds(sprite: arcade.Sprite):
    if sprite.left < 0:
        sprite.left = 0
    if sprite.right > MAP_WIDTH - 1:
        sprite.right = MAP_WIDTH - 1

    if sprite.bottom < 0:
        sprite.bottom = 0
    if sprite.top > MAP_HEIGHT - 1:
        sprite.top = MAP_HEIGHT - 1
