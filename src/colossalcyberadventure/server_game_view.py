import queue
import socket
import threading
from math import floor

import arcade
from arcade import Scene
from arcade import SpriteList
from arcade import key as k
from pyglet.math import Vec2
from pytiled_parser import parse_world

from . import enemies, player
from .camera import GameCam
from .enemies import Archer, ArcherAnimationState
from .enemies import Skeleton, SkeletonAnimationState
from .hud import HUD
from .item import Coin
from .player import Player, PlayerAnimationState
from .projectile import Projectile
from .server import messages
from .server.messages import create_movement_request, create_shoot_request
from .tilemap import tilemap_from_world, get_loader, init_loader


class ServerGameView(arcade.View):
    BACKGROUND_COLOR = arcade.color.JET
    WORLD_PATH = arcade.resources.resolve_resource_path(":data:map/map.world")
    TILEMAP_WIDTH_PX = 1920
    TILEMAP_HEIGHT_PX = 1080
    WORLD_WIDTH_TILEMAPS = 40
    WORLD_HEIGHT_TILEMAPS = 40

    def __init__(self, conn: socket.socket, player_id, coin_amount):
        super().__init__()

        # ------------------------------------------------------------
        init_loader()

        self.window.conn = conn
        self.conn = conn
        self.player_id = player_id
        self.keyboard_state = {k.W: False, k.A: False, k.S: False, k.D: False, k.C: False, k.H: False, k.Q: False,
                               k.I: False, k.V: False}

        self.bullet_target = (0.0, 0.0)
        self.on_shoot = False

        self.scene = arcade.Scene()
        # This whole part is just for the player and will be switched out eventually
        # All these sprite lists should remain empty
        # ------------------------------------------------------------------------------------------
        self.enemy_list = arcade.SpriteList()
        self.enemy_projectile_list = arcade.SpriteList()
        self.player_projectile_list = arcade.SpriteList()
        self.item_list = arcade.SpriteList()
        self.xp_list = arcade.SpriteList()
        # ------------------------------------------------------------------------------------------
        self.player = Player(self.enemy_projectile_list, self.player_projectile_list, self.item_list,
                             self.keyboard_state, self.scene, self.xp_list, coin_amount)
        self.entities = arcade.SpriteList(use_spatial_hash=True)

        self.entity_ids = dict()

        self.server_entity_list = []
        self.movement_vec = Vec2(0.0, 0.0)

        # map stuff:
        self.camera = GameCam(self.player)
        self.world = parse_world(ServerGameView.WORLD_PATH)
        self.non_drawn_scene = arcade.Scene()
        map_world_x, map_world_y = (
            floor(self.player.center_x / ServerGameView.TILEMAP_WIDTH_PX),
            floor(self.player.center_y / ServerGameView.TILEMAP_HEIGHT_PX),
        )
        self.connect_scenes(
            arcade.Scene.from_tilemap(
                tilemap_from_world(
                    map_world_x,
                    map_world_y,
                    self.world.maps[map_world_x * ServerGameView.WORLD_WIDTH_TILEMAPS + map_world_y].map_file,
                    ServerGameView.TILEMAP_WIDTH_PX,
                    ServerGameView.TILEMAP_HEIGHT_PX,
                )
            ),
            "0-0",
        )
        self.loader = get_loader()
        self.maps_in_loading = []
        self.hud = HUD(self.player, self.camera, self)

        # add entities to scene:
        # self.scene.add_sprite_list("entities", True, self.entities)

        # client stuff:
        server_handler = threading.Thread(target=handle_server, args=(conn, self))
        server_handler.start()

        arcade.set_background_color(ServerGameView.BACKGROUND_COLOR)

    def get_tilemap_file_from_world(self, x, y):
        return self.world.maps[x * ServerGameView.WORLD_WIDTH_TILEMAPS + y].map_file

    def connect_scenes(self, other_scene: Scene, key: str):
        tmp_spritelist = SpriteList()
        for spritelist in other_scene.sprite_lists:
            tmp_spritelist.extend(spritelist)
        self.scene.add_sprite_list(key, True, tmp_spritelist)

    def mouse_to_world_position(self, click_x: float, click_y: float) -> Vec2:
        """Converts the position of a click to the actual world position

        Parameters
        ----------
        click_x : float
        click_y : float

        Returns
        -------
        Vec2
            x -> world x, y -> world y
        """
        return Vec2(self.camera.position.x + click_x, self.camera.position.y + click_y)

    def on_draw(self):
        self.clear()
        self.scene.draw()
        self.camera.use()
        self.entities.draw()
        self.hud.draw()

    def on_update(self, delta_time: float):
        # updates entities:
        self.update_entities()

        for x, y in self.get_maps_surrounding_player():
            if x >= 0 and y >= 0:
                key = f"{x}-{y}"
                if not (key in self.maps_in_loading or key in self.scene.name_mapping.keys()):
                    self.maps_in_loading.append(key)
                    params = {
                        "x": x,
                        "y": y,
                        "map_file": self.world.maps[x * ServerGameView.WORLD_WIDTH_TILEMAPS + y].map_file,
                        "world_width_in_tilemaps": ServerGameView.WORLD_WIDTH_TILEMAPS,
                        "width_px": ServerGameView.TILEMAP_WIDTH_PX,
                        "height_px": ServerGameView.TILEMAP_HEIGHT_PX,
                    }
                    self.loader.queue_in.put(params)

        if not len(self.maps_in_loading) == 0:
            try:
                return_dict = self.loader.queue_out.get(block=False)
                tilemap = return_dict["tilemap"]
                x_offset = return_dict["x"]
                y_offset = return_dict["y"]
                self.connect_scenes(arcade.Scene.from_tilemap(tilemap), f"{x_offset}-{y_offset}")
                self.maps_in_loading.remove(f"{x_offset}-{y_offset}")
            except queue.Empty:
                pass

        if self.keyboard_state[k.Q]:
            quit()

        # player movement request:
        self.calculate_movement_vec()
        update_vec = self.movement_vec.normalize() * 5
        movement_request = create_movement_request(update_vec.x, update_vec.y)
        self.conn.send(movement_request.to_bytes_packed())

        # shooting:
        if self.on_shoot:
            shoot_request = create_shoot_request(self.bullet_target[0], self.bullet_target[1])
            self.conn.send(shoot_request.to_bytes_packed())
            self.on_shoot = False

        # camera shit:
        self.camera.center_camera_on_player()

        # updating the state and direction of all the entities:
        self.entities.update_animation()
        self.entities.on_update()

    def update_entities(self):
        last_frame_id_set = set(self.entity_ids)
        for entity in self.server_entity_list:
            if entity.id in last_frame_id_set:
                last_frame_id_set.remove(entity.id)
            animation_state = None
            direction = None
            is_not_item_or_projectile = None
            match entity.type:
                case "player":
                    # update current player x, y in ghost player class (yay legacy code)
                    if entity.id == self.player_id:
                        self.player.center_x = entity.x
                        self.player.center_y = entity.y
                    try:
                        self.c = self.entity_ids[entity.id]
                    except:
                        self.c = Player(self.enemy_projectile_list, self.player_projectile_list, self.item_list,
                                        self.keyboard_state, self.scene, self.xp_list, -1)
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
                case "archer":
                    try:
                        self.c = self.entity_ids[entity.id]
                    except:
                        self.c = Archer(self.player, self.enemy_list, self.enemy_projectile_list,
                                        self.player_projectile_list, self.xp_list)
                        self.entities.append(self.c)
                        temp_dict = {entity.id: self.c}
                        self.entity_ids.update(temp_dict)
                    animation_state = ArcherAnimationState
                    direction = enemies.Direction
                case "bullet":
                    try:
                        self.c = self.entity_ids[entity.id]
                    except:
                        self.c = Projectile(entity.x, entity.y, self.bullet_target[0], self.bullet_target[1], ":data"
                                                                                                              ":bullet"
                                                                                                              "/0.png"
                                            , 1)
                        self.entities.append(self.c)
                        temp_dict = {entity.id: self.c}
                        self.entity_ids.update(temp_dict)
                    is_not_item_or_projectile = True
                case "coin":
                    try:
                        self.c = self.entity_ids[entity.id]
                    except:
                        self.c = Coin(entity.x, entity.y)
                        self.entities.append(self.c)
                        temp_dict = {entity.id: self.c}
                        self.entity_ids.update(temp_dict)
                    is_not_item_or_projectile = True

            self.c.center_x = entity.x
            self.c.center_y = entity.y
            if not is_not_item_or_projectile:
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

        if len(last_frame_id_set) > 0:
            for entity_id in last_frame_id_set:
                self.entities.remove(self.entity_ids[entity_id])
                self.entity_ids.pop(entity_id)

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol in self.keyboard_state.keys():
            self.keyboard_state[symbol] = True

    def on_key_release(self, symbol: int, _modifiers: int):
        if symbol in self.keyboard_state.keys():
            self.keyboard_state[symbol] = False

    def calculate_movement_vec(self):
        self.movement_vec.x = 0
        self.movement_vec.y = 0
        if self.keyboard_state[k.W]:
            self.movement_vec.y += 1
        if self.keyboard_state[k.S]:
            self.movement_vec.y += -1
        if self.keyboard_state[k.A]:
            self.movement_vec.x += -1
        if self.keyboard_state[k.D]:
            self.movement_vec.x += 1

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        world_pos = self.mouse_to_world_position(x, y)
        self.bullet_target = (world_pos.x, world_pos.y)
        self.on_shoot = True

    def get_maps_surrounding_player(self):
        min_x = floor((self.player.center_x - ServerGameView.TILEMAP_WIDTH_PX // 2) // ServerGameView.TILEMAP_WIDTH_PX)
        min_y = floor(
            (self.player.center_y - ServerGameView.TILEMAP_HEIGHT_PX // 2) // ServerGameView.TILEMAP_HEIGHT_PX)
        max_x = floor((self.player.center_x + ServerGameView.TILEMAP_WIDTH_PX // 2) // ServerGameView.TILEMAP_WIDTH_PX)
        max_y = floor(
            (self.player.center_y + ServerGameView.TILEMAP_HEIGHT_PX // 2) // ServerGameView.TILEMAP_HEIGHT_PX)
        return (min_x, min_y), (min_x, max_y), (max_x, max_y), (max_x, min_y)

    def remove_maps_outside_player_area(self):
        keys_to_remove = []
        maps = self.get_maps_surrounding_player()
        for key in self.scene.name_mapping.keys():
            x, y = map(lambda num: int(num), key.split("-"))
            if not (x, y) in maps:
                keys_to_remove.append(key)
        for key in keys_to_remove:
            self.scene.remove_sprite_list_by_name(key)


def handle_server(conn: socket.socket, view: ServerGameView):
    while True:
        server_update = messages.read_server_update(conn.recv(2048))
        match server_update.which():
            case "entitiesUpdate":
                view.server_entity_list = server_update.entitiesUpdate
            case "itemAdditionUpdate":
                match server_update.itemAdditionUpdate.item:
                    case "coin":
                        view.player.coin_counter += server_update.itemAdditionUpdate.change
