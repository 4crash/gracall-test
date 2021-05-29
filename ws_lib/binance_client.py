
import json
from asyncio import Queue
import asyncio
from typing import Dict
import sys
import websockets 
from singleton import Singleton
sys.path.append("../")
import logging
from settings import settings
# from ql_types import OrderSide
# from ql_types.finance import LimitPrice, Quantity

# import qutils.settings as qs

# from orderbook.orderbook import UniqueIdOrderBook
# from binance_app.binance_structs import BinanceSnapshot,BinanceStream



# ob: UniqueIdOrderBook = UniqueIdOrderBook()

# settings = qs.load("dev")
# print(settings)


class BinanceClient(Singleton):
    
    def __init__(self) -> None:
        self.ping_timeout = 2
        self.sleep_time = 5
        # self.streaming = True
       
    async def start_stream(self, q_data: Queue, symbol:str="btcusdt") -> None:
        
        stream_url = settings.binance_stream_url.format(symbol=symbol)
                
        while True:
            # reconnect when failed
            try:
                async with websockets.connect(stream_url) as ws:
                    while True:
                        
                        data = await ws.recv()
                        json_l = json.loads(data)
                        await q_data.put(json_l)
                        try:
                            reply = await asyncio.wait_for(ws.recv(), timeout=self.ping_timeout)
                        except (asyncio.TimeoutError, websockets.exceptions.ConnectionClosed):
                            try:
                                pong = await ws.ping()
                                await asyncio.wait_for(pong, timeout=self.ping_timeout)
                                logging.debug(
                                    'Ping OK, keeping connection alive...')
                                continue
                            except:
                                await asyncio.sleep(self.sleep_time)
                                break  # inner loop
                        # do stuff with reply object
            except ConnectionRefusedError:
                logging.warning("cannot connect to binance")
                await asyncio.sleep(self.sleep_time)
                continue
            # receive
           
          
                
    async def print_data_test(self, queue:Queue) -> None:
        while True:
            data = await queue.get()
            # json_l = json.loads(data)
            price = data["b"][0][0]
            print(price)
            # json_l = json.load(data)
                  
    async def main(self):
        q: asyncio.Queue = asyncio.Queue()
        tasks = []
        tasks.append(asyncio.create_task(bc.start_stream(q)))
        tasks.append(asyncio.create_task(bc.print_data_test(q)))
        await asyncio.gather(*tasks)
        
          
if __name__ == "__main__":
    
    bc = BinanceClient()
    asyncio.run(bc.main())
   
