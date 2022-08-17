import asyncio
import socket


class EchoClientProtocol(asyncio.Protocol):
    def __init__(self, message, on_con_lost):
        self.message = message
        self.on_con_lost = on_con_lost

    def connection_made(self, transport):
        transport.write(self.message.encode())
        print('Data sent: {!r}'.format(self.message))

    def data_received(self, data):
        print('Data received: {!r}'.format(data.decode()))

    def connection_lost(self, exc):
        print('The server closed the connection')
        self.on_con_lost.set_result(True)



async def main():
    # Get a reference to the event loop as we plan to use
    # low-level APIs.
    loop = asyncio.get_running_loop()

    on_con_lost = loop.create_future()
    message = 'Hello World!'

    transport, protocol = await loop.create_connection(
        protocol_factory=lambda: EchoClientProtocol(message, on_con_lost),
        host='127.0.0.1', 
        port=8888,
        #local_addr=('127.0.0.1', 9889)
    )

    print()
    print(f"Server socket: {transport.get_extra_info('peername')}")
    print(f"Client socket: {transport.get_extra_info('sockname')}")

    try:
        await on_con_lost
    finally:
        transport.close()
    

asyncio.run(main())

