import asyncio
import time

import httpx
from quart import Quart, request

app = Quart(__name__)

async def _background_task(timeout):
    async with httpx.AsyncClient() as client:
        response = await client.get('http://0.0.0.0:5000/test')
        print("Response from test route", response.text)
    #await asyncio.sleep(timeout)
    print("I am completed")
 
@app.route("/", methods=["POST", "GET"])
async def main_route():
    print("Hello from main route")
    #await asyncio.sleep(1)
    app.add_background_task(_background_task, 10)
    return "Hello from root"

@app.route("/test", methods=["POST", "GET"])
async def test_route():
    print("Hello from test route")
    #await asyncio.sleep(0.5)
    return "Hello from test" + str(time.time())

if __name__ == '__main__':
    from hypercorn.config import Config
    from hypercorn.asyncio import serve

    Config.bind = ["0.0.0.0:5000"]
    asyncio.run(serve(app, Config()))