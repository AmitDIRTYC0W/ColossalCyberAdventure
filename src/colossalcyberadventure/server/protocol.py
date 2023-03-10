import asyncio

from aioquic.asyncio import QuicConnectionProtocol
from aioquic.quic import events
from aioquic.quic.events import StreamDataReceived

from src.colossalcyberadventure.server.messages import create_identification_request, read_identification_response


class IdentificationProtocol(QuicConnectionProtocol):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._ack_waiter = None
        self.response = None

    def quic_event_received(self, event: events.QuicEvent) -> None:
        if self._ack_waiter is not None:
            if isinstance(event, StreamDataReceived):
                self.response = read_identification_response(event.data)
                waiter = self._ack_waiter
                self._ack_waiter = None
                waiter.set_result(self.response)

    async def send_identification(self, username, password, register):
        stream_id = self._quic.get_next_available_stream_id()
        data = create_identification_request(username, password, register).to_bytes_packed()
        self._quic.send_stream_data(stream_id, data, end_stream=False)
        waiter = self._loop.create_future()
        self._ack_waiter = waiter
        self.transmit()

        return await asyncio.shield(waiter)
