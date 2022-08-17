import asyncio
import aiohttp

async def main():
    async with aiohttp.ClientSession() as session:
        async with session.get('http://localhost:8080/remote') as resp:
            print(resp.status)
            print(await resp.text())

asyncio.run(main)