import asyncio


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



class Clients:

    async def start_server(self, host, port):
        self.host = host
        self.port = port
        self.server = await asyncio.start_server(
            client_connected_cb=self.handle_echo, 
            host=host, 
            port=port
        )
        async with self.server:
            await self.server.serve_forever()

    async def handle_echo(reader, writer):
        data = await reader.read(100)
        message = data.decode()
        addr = writer.get_extra_info('peername')

        print(f"Received {message!r} from {addr!r}")

        print(f"Send: {message!r}")
        writer.write(data)
        await writer.drain()

        print("Close the connection")
        writer.close()


    async def write(self, host, port, message):
        loop = self.server.get_loop()
        
        on_con_lost = loop.create_future()

        transport, protocol = await loop.create_connection(
            protocol_factory=lambda: EchoClientProtocol(message, on_con_lost),
            host=host, 
            port=port,
            local_addr=(self.host, self.port)
        )

        print()
        print(f"Server socket: {transport.get_extra_info('peername')}")
        print(f"Client socket: {transport.get_extra_info('sockname')}")

        try:
            await on_con_lost
        finally:
            transport.close()


        # print(sock.getsockname())
        # print(sock.getpeername())
        # reader, writer = await asyncio.open_connection(
        #     host=host, 
        #     port=port,
        # )

        # print(f'Send: {message!r}')
        # writer.write(message.encode())

        # data = await reader.read(100)
        # print(f'Received: {data.decode()!r}')

        # print('Close the connection')
        # writer.close()


# async def tcp_echo_client1(message):
#     reader, writer = await asyncio.open_connection(
#         '127.0.0.1', 8888)

#     print(f'Send: {message!r}')
#     writer.write(message.encode())

#     data = await reader.read(100)
#     print(f'Received: {data.decode()!r}')

#     print('Close the connection')
#     writer.close()

async def main():
    client1 = Clients()
    task1 = asyncio.create_task(client1.start_server('127.0.0.1', 8888))
    await asyncio.sleep(1)
    task2 = asyncio.create_task(client1.write('127.0.0.1', 9999, 'hello'))
    tasks = [task1, task2]
    await asyncio.gather(*tasks)
    


asyncio.run(main())
