import os

from aioquic.quic.configuration import QuicConfiguration


print(os.getcwd())
CERT_PATH = "./server/cert.pem"
CONFIGURATION = QuicConfiguration(is_client=True, alpn_protocols=["ccam/2.0"])
CONFIGURATION.load_verify_locations(CERT_PATH)
