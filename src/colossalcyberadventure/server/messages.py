import capnp

capnp.remove_import_hook()
log_in_capnp = capnp.load("../../../submodules/ColossalCyberAdventureMessages/log_in.capnp")


def create_login_request(username, password):
    return log_in_capnp.LogInRequest.new_message(username=username, password=password)


def read_login_response(b: bytes):
    return log_in_capnp.LogInResponse.from_bytes_packed(b)
