
import asyncio
import clients

async def main2():
    client = clients.Clients()
    task1 = asyncio.create_task(client.start_server('127.0.0.1', 9999))
    
    await asyncio.gather(task1)
    

asyncio.run(main2())