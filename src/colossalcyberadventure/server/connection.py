from typing import cast

from aioquic.quic.configuration import QuicConfiguration
from aioquic.asyncio import connect

from colossalcyberadventure.server.protocol import LogInProtocol

CERT_PATH = "TODO"
CONFIGURATION = QuicConfiguration(is_client=True, alpn_protocols=["ccam/2.0"])
CONFIGURATION.load_verify_locations(CERT_PATH)


async def establish_connection(addr, config: QuicConfiguration = CONFIGURATION):
    async with connect(addr, configuration=config, create_protocol=LogInProtocol) as client:
        client = cast(LogInProtocol, client)
