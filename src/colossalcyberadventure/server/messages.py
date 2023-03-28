import capnp

capnp.remove_import_hook()

server_update_capnp = capnp.load(
    "../../submodules/ColossalCyberAdventureMessages/src/colossalcyberadventuremessages/server_update.capnp"
)
client_update_capnp = capnp.load(
    "../../submodules/ColossalCyberAdventureMessages/src/colossalcyberadventuremessages/client_update.capnp"
)


def read_server_update(b: bytes):
    return server_update_capnp.ServerUpdate.from_bytes_packed(b)


def create_movement_request(x: float, y: float):
    return client_update_capnp.ClientUpdate.new_message(move=client_update_capnp.Move.new_message(x=x, y=y))
