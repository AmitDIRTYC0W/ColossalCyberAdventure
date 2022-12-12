from entity import IEntity
from arcade import Sprite


class Player(IEntity, Sprite):
    def __init__(self):
        super().__init__()
