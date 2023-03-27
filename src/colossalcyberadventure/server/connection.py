from typing import cast

from aioquic.asyncio import connect
from aioquic.quic.configuration import QuicConfiguration

from src.colossalcyberadventure.server.protocol import IdentificationProtocol

CERT_PATH = "./server/cert.pem"
TIMEOUT_LEN = 2.0


async def connect_to_server(host: str, port: int, username: str, password: str, register: bool):
    config = QuicConfiguration(is_client=True, alpn_protocols=['ccam/0.1'], idle_timeout=TIMEOUT_LEN)
    config.load_verify_locations(CERT_PATH)
    c = connect(host, port, configuration=config, create_protocol=IdentificationProtocol, wait_connected=True)
    try:
        async with c as client:
            client = cast(IdentificationProtocol, client)
            resp = await client.send_identification(username, password, register)
            if resp.which() == "success":
                return c
            else:
                return None
    except ConnectionError:
        return None
