from asyncio.tasks import Task
from typing import List
import websockets
from main import app
from fastapi.testclient import TestClient
import asyncio
client = TestClient(app)
import pytest


@pytest.mark.skip("not finished yet")
def test_ws():
    async def connect(q: asyncio.Queue):
        try:
            async with websockets.connect("ws://127.0.0.1:8000/ws") as ws:
                json = {
                    "command": "start",
                    "symbol": "btcusdt",
                }
                ws.send(json)
                data = await ws.recv()
                q.put(data)
                json = {
                    "command": "stop",
                    "symbol": "btcusdt",
                }
                print(data)
                assert data is not None, "no data "
                assert data.get("symbol") is not None, "Received data wrong format"
        except KeyboardInterrupt:
            print("Canceled")
    
    async def receive_data(q: asyncio.Queue, task:Task):
        while True:
            data = await q.get()
            print(data)
            task.cancel()
            break
    
    async def run():
        try:
            q = asyncio.Queue()
            tasks:List[Task]= []
            # make connection attempt
            tasks.append(await asyncio.wait_for(connect(q),10))
            tasks.append(await asyncio.create_task(receive_data(q)))
            return asyncio.gather(tasks)
        except KeyboardInterrupt:
            pass
      
    
    asyncio.run(run())

        
