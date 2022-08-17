import asyncio

class EchoServerProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        sockname = transport.get_extra_info('sockname')
        peername = transport.get_extra_info('peername')
        print(f'Server socket: {sockname}')
        print(f'Client socket: {peername}')
        self.transport = transport

    def data_received(self, data):
        message = data.decode()
        print(f'Data received: {message}')

        print('Send to client: {!r}'.format(message))
        self.transport.write(data)

        print('Close the client socket')
        self.transport.close()


async def main():
    # Get a reference to the event loop as we plan to use
    # low-level APIs.
    loop = asyncio.get_running_loop()

    server = await loop.create_server(
        protocol_factory=lambda: EchoServerProtocol(),
        host='127.0.0.1', 
        port=8889
    )

    async with server:
        await server.serve_forever()

    

asyncio.run(main())