from colossalcyberadventuremessages import server_update, client_update, identification


def read_server_update(b: bytes):
    return server_update.ServerUpdate.from_bytes_packed(b)


def create_movement_request(x: float, y: float):
    return client_update.ClientUpdate.new_message(move=client_update.Move.new_message(x=x, y=y))


def create_shoot_request(x: float, y: float):
    return client_update.ClientUpdate.new_message(shot=client_update.Shot.new_message(x=x, y=y))


def create_skill_use_request(skill_num: int):
    return client_update_capnp.ClientUpdate.new_message(useSkill=skill_num)


def create_identification_request(username: str, password: str, register: bool):
    return identification.IdentificationRequest.new_message(
        username=username,
        password=password,
        register=register
    )


def read_identification_response(b: bytes):
    return identification.IdentificationResponse.from_bytes_packed(b)
