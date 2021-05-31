import asyncio as aio
from typing import List
from ws_lib.binance_client import BinanceClient 
import logging

def test_binance_client():
     # q: aio.Queue = aio.Queue()
    # tasks: List[aio.Task] = []
    # bc = BinanceClient()
    # await aio.run(await aio.wait_for(bc.start_stream(q),5))

    async def print_data_test(queue: aio.Queue, task: aio.Task) -> None:
        while True:
            data = await queue.get()
            # json_l = json.loads(data)
            price = data["b"][0][0]
            # logging.debug(price)
           
            task.cancel()
            return data

      

    async def main():
        q: aio.Queue = aio.Queue()
        tasks: List[aio.Task] = []
        tasks.append(aio.create_task(bc.start_stream(q)))
        tasks.append(aio.create_task(print_data_test(q, tasks[0])))
        results = await aio.gather(*tasks)
        return results


        
    bc = BinanceClient()
    
    try:
        results = aio.run(main())
        assert results is not None, "Data doesnt exists"
        assert float(results[1]["b"][0][0]) > 0, "data is in wrong format"

    except aio.exceptions.CancelledError as e:
        logging.warning("Task was canceled")
        
    
