import socket
import threading

import arcade
from pyglet.math import Vec2

from . import enemies, player
from .enemies import Skeleton, SkeletonAnimationState
from .player import Player, PlayerAnimationState, Direction
from .server import messages
from .server.messages import create_movement_request


class ServerGameView(arcade.View):
    def __init__(self, conn: socket.socket):
        super().__init__()

        self.conn = conn

        self.scene = arcade.Scene()
        # This whole part is just for the player and will be switched out eventually
        # All these sprite lists should remain empty
        # ------------------------------------------------------------------------------------------
        self.enemy_list = arcade.SpriteList()
        self.enemy_projectile_list = arcade.SpriteList()
        self.player_projectile_list = arcade.SpriteList()
        self.item_list = arcade.SpriteList()
        self.xp_list = arcade.SpriteList()
        self.keyboard_state = {}
        # ------------------------------------------------------------------------------------------
        self.player = Player(self.enemy_projectile_list, self.player_projectile_list, self.item_list,
                             self.keyboard_state, self.scene, self.xp_list)
        self.entities = arcade.SpriteList()
        self.scene.add_sprite_list("entities", True, self.entities)

        self.entity_ids = dict()

        self.server_entity_list = []
        self.movement_vec = Vec2(0.0, 0.0)

        server_handler = threading.Thread(target=handle_server, args=(conn, self))
        server_handler.start()

        arcade.set_background_color(arcade.color.AMAZON)

    def on_draw(self):
        self.clear()
        self.scene.draw()

    def on_update(self, delta_time: float):
        self.update_entities()

        # player movement request:
        update_vec = self.movement_vec.normalize() * 5
        movement_request = create_movement_request(update_vec.x, update_vec.y)
        self.conn.send(movement_request.to_bytes_packed())

        # updating the state and direction of all the entities:
        self.entities.update_animation()
        self.entities.on_update()

    def update_entities(self):
        for entity in self.server_entity_list:  # ToDO make it so the entity gets deleated when it is no longer given to you...
            print(entity.x, entity.y)
            animation_state = None
            direction = None
            match entity.type:
                case "player":
                    try:
                        self.c = self.entity_ids[entity.id]
                    except:
                        self.c = Player(self.enemy_projectile_list, self.player_projectile_list, self.item_list,
                                        self.keyboard_state, self.scene, self.xp_list)
                        self.entities.append(self.c)
                        temp_dict = {entity.id: self.c}
                        self.entity_ids.update(temp_dict)
                    animation_state = PlayerAnimationState
                    direction = player.Direction
                case "skeleton":
                    try:
                        self.c = self.entity_ids[entity.id]
                    except:
                        self.c = Skeleton(self.player, self.enemy_list, self.enemy_projectile_list,
                                          self.player_projectile_list, self.xp_list)
                        self.entities.append(self.c)
                        temp_dict = {entity.id: self.c}
                        self.entity_ids.update(temp_dict)
                    animation_state = SkeletonAnimationState
                    direction = enemies.Direction
            self.c.center_x = entity.x
            self.c.center_y = entity.y
            match entity.animationstate:
                case "idle":
                    self.c.animation_state = animation_state.IDLE
                case "walk":
                    self.c.animation_state = animation_state.WALK
                case "attack":
                    self.c.animation_state = animation_state.ATTACK
                case "death":
                    self.c.animation_state = animation_state.DEATH
            match entity.direction:
                case "left":
                    self.c.direction = direction.LEFT
                case "right":
                    self.c.direction = direction.RIGHT

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.W:
            self.movement_vec.y = 1
        elif symbol == arcade.key.S:
            self.movement_vec.y = -1
        elif symbol == arcade.key.A:
            self.movement_vec.x = -1
        elif symbol == arcade.key.D:
            self.movement_vec.x = 1

    def on_key_release(self, symbol: int, _modifiers: int):
        if symbol == arcade.key.W:
            self.movement_vec.y = 0
        elif symbol == arcade.key.S:
            self.movement_vec.y = 0
        elif symbol == arcade.key.A:
            self.movement_vec.x = 0
        elif symbol == arcade.key.D:
            self.movement_vec.x = 0


def handle_server(conn: socket.socket, view: ServerGameView):
    while True:
        server_update = messages.read_server_update(conn.recv(2048))
        print(server_update)
        view.server_entity_list = server_update.entitiesUpdate
