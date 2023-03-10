import capnp

capnp.remove_import_hook()
identification_capnp = capnp.load(
    "../../submodules/ColossalCyberAdventureMessages/src/colossalcyberadventuremessages/identification.capnp")


def create_identification_request(username, password, register):
    return identification_capnp.IdentificationRequest.new_message(
        username=username, password=password, register=register)


def read_identification_response(b: bytes):
    return identification_capnp.IdentificationResponse.from_bytes_packed(b)
