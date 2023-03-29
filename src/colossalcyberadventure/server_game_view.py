import socket
import threading

import arcade
from pyglet.math import Vec2

from .enemies import Skeleton
from .player import Player
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
        for entity in self.server_entity_list:
            match entity.type:
                case "player":
                    # TODO VERY IMPORTANT!!! Make it so the entities are not recreated each time - use sets for O(n)
                    try:
                        p = self.entity_ids[entity.id]
                        p.center_x = entity.x
                        p.center_y = entity.y
                    except:
                        p = Player(self.enemy_projectile_list, self.player_projectile_list, self.item_list,
                                   self.keyboard_state, self.scene, self.xp_list)
                        p.center_x = entity.x
                        p.center_y = entity.y
                        self.entities.append(p)
                        temp_dict = {entity.id: p}
                        self.entity_ids.update(temp_dict)
                case "skeleton":
                    try:
                        skeleton = self.entity_ids[entity.id]
                        skeleton.center_x = entity.x
                        skeleton.center_y = entity.y
                    except:
                        skeleton = Skeleton(self.player, self.enemy_list, self.enemy_projectile_list,
                                            self.player_projectile_list, self.xp_list)
                        skeleton.center_x = entity.x
                        skeleton.center_y = entity.y
                        self.entities.append(skeleton)
                        temp_dict = {entity.id: skeleton}
                        self.entity_ids.update(temp_dict)

        self.player.center_x += (self.movement_vec.normalize() * 5).x
        self.player.center_y += (self.movement_vec.normalize() * 5).y
        movement_request = create_movement_request(self.player.center_x, self.player.center_y)
        self.conn.send(movement_request.to_bytes_packed())

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
        view.server_entity_list = server_update.entitiesUpdate
