import asyncio as aio
from asyncio.exceptions import CancelledError
from typing import List
from ws_lib.binance_client import BinanceClient 
import pytest

@pytest.mark.skip(reason=" Not finished by the best practices. How to correctly test infinity loop?")
def test_binance_client():
    
    async def print_data_test( queue: aio.Queue, task:aio.Task) -> None:
        while True:
            data = await queue.get()
            # json_l = json.loads(data)
            price = data["b"][0][0]
            print(price)
            
            break
        
        task.cancel()
        return price

    async def main():
        q: aio.Queue = aio.Queue()
        tasks:List[aio.Task] = []
        tasks.append(aio.create_task(bc.start_stream(q)))
        tasks.append(aio.create_task(print_data_test(q, tasks[0])))
        await aio.gather(*tasks)
        
    bc = BinanceClient()
    
    try:
        results = aio.run(main())
    except aio.exceptions.CancelledError as e:
        print(e)
        
    assert results is not None
