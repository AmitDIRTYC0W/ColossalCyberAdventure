import queue
import random
import socket
import threading
import time
from math import floor

import arcade
from arcade import Scene, Text
from arcade import SpriteList
from arcade import key as k
from pyglet.math import Vec2
from pytiled_parser import parse_world

from . import enemies, player, constants
from .camera import GameCam
from .death_screen import DeathScreenView
from .enemies import Archer, ArcherAnimationState
from .enemies import Skeleton, SkeletonAnimationState
from .healthbar import HealthBar
from .hud import HUD
from .item import Coin, HealthShroom
from .player import Player, PlayerAnimationState
from .projectile import Projectile
from .server import messages
from .server.messages import create_movement_request, create_shoot_request, create_skill_use_request
from .tilemap import tilemap_from_world, get_loader, init_loader
from .xp import XP

textures = set()


class ServerGameView(arcade.View):
    BACKGROUND_COLOR = arcade.color.JET
    WORLD_PATH = arcade.resources.resolve_resource_path(":data:map/map.world")
    TILEMAP_WIDTH_PX = 1920
    TILEMAP_HEIGHT_PX = 1080
    WORLD_WIDTH_TILEMAPS = 40
    WORLD_HEIGHT_TILEMAPS = 40

    def __init__(self, conn: socket.socket, player_id, coin_amount, xp_amount, mushroom_amount, hp):
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
        self.xp = xp_amount
        self.player = Player(self.enemy_projectile_list, self.player_projectile_list, self.item_list,
                             self.keyboard_state, self.scene, self.xp_list, coin_amount, xp_amount, mushroom_amount)
        self.entities = arcade.SpriteList(use_spatial_hash=True)
        self.start_bot = 0
        self.bot_on = False

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
        self.health_bar = HealthBar(self.player, 70, 5, 1, arcade.color.BLACK, arcade.color.RED)
        self.health_bar.health_points = hp

        self.level_text = Text(f"Level: {self.player.level}", self.player.center_x - self.player.width // 2,
                               self.player.center_y + HealthBar.LEVEL_TEXT_OFFSET, arcade.color.JET)

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
            constants.texture_holder.update(spritelist)
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
        self.health_bar.draw()

    def on_update(self, delta_time: float):
        # updates entities:
        self.update_entities()
        self.health_bar.on_update()

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

        # close:
        if self.keyboard_state[k.Q]:
            self.conn.close()
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

        # skill checks...
        if self.keyboard_state[k.C]:
            skill_request = create_skill_use_request(1)
            self.conn.send(skill_request.to_bytes_packed())
            self.keyboard_state[k.C] = False

        if self.keyboard_state[k.H]:
            skill_request = create_skill_use_request(2)
            self.conn.send(skill_request.to_bytes_packed())
            self.keyboard_state[k.H] = False

        if self.keyboard_state[k.V]:
            skill_request = create_skill_use_request(3)
            self.conn.send(skill_request.to_bytes_packed())
            self.keyboard_state[k.V] = False

        # check death:
        if self.health_bar.health_points <= 0:
            self.conn.close()
            self.window.show_view(DeathScreenView())

        # camera shit:
        self.camera.center_camera_on_player()

        # updating the state and direction of all the entities:
        self.entities.update_animation()
        self.entities.on_update()

        constants.texture_holder.update(self.entities)

    def update_entities(self):
        global textures
        last_frame_id_set = set(self.entity_ids)
        for entity in self.server_entity_list:
            if entity.id in last_frame_id_set:
                last_frame_id_set.remove(entity.id)
            animation_state = None
            direction = None
            is_item_or_projectile = False
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
                                        self.keyboard_state, self.scene, None, 100, self.xp, 100)
                        textures.add(self.c)
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
                        textures.add(self.c)
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
                        textures.add(self.c)
                        self.entities.append(self.c)
                        temp_dict = {entity.id: self.c}
                        self.entity_ids.update(temp_dict)
                    animation_state = ArcherAnimationState
                    direction = enemies.Direction
                case "playerBullet":
                    try:
                        self.c = self.entity_ids[entity.id]
                    except:
                        self.c = Projectile(entity.x, entity.y, self.bullet_target[0], self.bullet_target[1],
                                            ":data:bullet/0.png", 1)
                        textures.add(self.c)
                        self.entities.append(self.c)
                        temp_dict = {entity.id: self.c}
                        self.entity_ids.update(temp_dict)
                    is_item_or_projectile = True

                case "archerBullet":
                    try:
                        self.c = self.entity_ids[entity.id]
                    except:
                        self.c = Projectile(entity.x, entity.y, self.bullet_target[0], self.bullet_target[1],
                                            ":data:enemies/archer/arrow/0.png", 2)
                        textures.add(self.c)
                        self.entities.append(self.c)
                        temp_dict = {entity.id: self.c}
                        self.entity_ids.update(temp_dict)
                    is_item_or_projectile = True

                case "coin":
                    try:
                        self.c = self.entity_ids[entity.id]
                    except:
                        self.c = Coin(entity.x, entity.y)
                        textures.add(self.c)
                        self.entities.append(self.c)
                        temp_dict = {entity.id: self.c}
                        self.entity_ids.update(temp_dict)
                    is_item_or_projectile = True
                case "xp":
                    try:
                        self.c = self.entity_ids[entity.id]
                    except:
                        self.c = XP(entity.x, entity.y)
                        textures.add(self.c)
                        self.entities.append(self.c)
                        temp_dict = {entity.id: self.c}
                        self.entity_ids.update(temp_dict)
                    is_item_or_projectile = True
                case "mushroom":
                    try:
                        self.c = self.entity_ids[entity.id]
                    except:
                        self.c = HealthShroom(entity.x, entity.y)
                        textures.add(self.c)
                        self.entities.append(self.c)
                        temp_dict = {entity.id: self.c}
                        self.entity_ids.update(temp_dict)
                    is_item_or_projectile = True

            self.c.center_x = entity.x
            self.c.center_y = entity.y
            if not is_item_or_projectile:
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
        if symbol == k.B:
            self.bot_on = not self.bot_on
        if symbol in self.keyboard_state.keys():
            self.keyboard_state[symbol] = True
        if symbol == arcade.key.I:
            self.hud.shown = not self.hud.shown
        if symbol == arcade.key.Z:
            mushroom_use_request = messages.create_item_use_request("mushroom")
            self.conn.send(mushroom_use_request.to_bytes_packed())

    def on_key_release(self, symbol: int, _modifiers: int):
        if symbol in self.keyboard_state.keys():
            self.keyboard_state[symbol] = False

    def calculate_movement_vec(self):
        if self.bot_on:
            if time.time() - self.start_bot > 6:
                self.start_bot = time.time()
                choice = 0
                while choice == 0:
                    choice = random.randint(-1, 1)
                if random.random() > 0.5:
                    if self.player.center_x > 1000:
                        self.movement_vec = Vec2(choice, 0)
                    else:
                        self.movement_vec = Vec2(1, 0)
                else:
                    if self.player.center_y > 1000:
                        self.movement_vec = Vec2(0, choice)
                    else:
                        self.movement_vec = Vec2(0, 1)

        # if self.keyboard_state[k.B]:
        #     self.start_bot = time.gmtime(0)
        #     self.movement_vec = Vec2(random.randint(10, 100))
        else:
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
            case "healthPoints":
                view.health_bar.health_points = server_update.healthPoints.hp
            case "itemAdditionUpdate":
                match server_update.itemAdditionUpdate.item:
                    case "coin":
                        view.player.coin_counter = server_update.itemAdditionUpdate.amount
                    case "xp":
                        view.xp = server_update.itemAdditionUpdate.amount
                    case "mushroom":
                        view.player.mushroom_amount = server_update.itemAdditionUpdate.amount
