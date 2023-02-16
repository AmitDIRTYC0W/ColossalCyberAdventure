import asyncio

from aioquic.asyncio import QuicConnectionProtocol
from aioquic.quic import events
from aioquic.quic.events import StreamDataReceived

from colossalcyberadventure.server.messages import create_login_request, read_login_response


class LogInProtocol(QuicConnectionProtocol):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._ack_waiter = None
        self.response = None

    def quic_event_received(self, event: events.QuicEvent) -> None:
        if self._ack_waiter is not None:
            if isinstance(event, StreamDataReceived):
                self.response = read_login_response(event.data)

    async def send_log_in(self, username, password):
        stream_id = self._quic.get_next_available_stream_id()
        data = create_login_request(username, password).to_bytes_packed()
        self._quic.send_stream_data(stream_id, data, end_stream=True)
        waiter = self._loop.create_future()
        self._ack_waiter = waiter
        self.transmit()

        return await asyncio.shield(waiter)
