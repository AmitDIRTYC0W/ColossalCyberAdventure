import arcade
import math

from src.colossalcyberadventure.entity import IEntity
from src.colossalcyberadventure.player import Player

BULLET_SPRITE = "resources/shot.png"
BULLET_SPEED = 9


class Bullet(arcade.Sprite, IEntity):
    def __init__(self):
        super().__init__(filename=BULLET_SPRITE)
        self.distance_traveled: float = 0

    def get_position(self):
        return self.center_x, self.center_y

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y

    def shot(self, player: Player, mouse_x: float, mouse_y: float):
      # Here is the function I want you to rewrite, Ignore my shitty spaghetti code!
      # self.center_x = player.center_x

      #self.center_y = player.center_y

      ## finding the angel that the bullet should travel in using math.atan2
      #delta_x = mouse_x
      #delta_y = mouse_y

      #print(delta_x, delta_y)


      #self.angle = math.degrees(math.atan2(delta_y, delta_x))

      ## moving the bullet
      #rad = math.radians(self.angle)
      #self.change_x = math.cos(rad) * BULLET_SPEED
      #self.change_y = math.sin(rad) * BULLET_SPEED

#option 2 : distance - only

