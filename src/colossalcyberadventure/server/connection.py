from typing import cast

from aioquic.quic.configuration import QuicConfiguration
from aioquic.asyncio import connect

from src.colossalcyberadventure.server.protocol import IdentificationProtocol

CERT_PATH = "./certificate.pem"
CONFIGURATION = QuicConfiguration(is_client=True, alpn_protocols=["ccam/2.0"])
CONFIGURATION.load_verify_locations(CERT_PATH)


# async def establish_connection(addr, config: QuicConfiguration = CONFIGURATION):
#     async with connect(addr, configuration=config, create_protocol=IdentificationProtocol) as client:
#         client = cast(IdentificationProtocol, client)
