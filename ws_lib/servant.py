import asyncio as aio
from typing import Dict, List
from ws_lib.binance_client import BinanceClient
from fastapi import WebSocket
import json
from dataclasses import dataclass
import logging
from settings import settings


@dataclass
class CryptoRequest:
    symbol: str
    command: str
    

class WSServant():
    def __init__(self, websocket:WebSocket):
        self.websocket = websocket
        
        
    
    async def receive(self, queue: aio.Queue)->None:
        
        while True:
            data = await queue.get()
            try:
                binance_json = {
                    "symbol": data["s"],
                    "price": data["b"][0][0],
                    "quantity": data["b"][0][1]
                    
                }
            except IndexError as e:
                logging.warning(e)
                
            try:
                await self.websocket.send_json(binance_json)
            except RuntimeError as e:
                logging.warning(e)
                
            
                    

    async def commander(self,data_q:aio.Queue, loop:aio.AbstractEventLoop)->None:
        
        await self.websocket.accept()
        bc = BinanceClient()
        tasks:Dict[str,aio.Task] = {}
        
        try:
            while True:
                data = await self.websocket.receive()
               
                message = data.get("text")
                if message is not None:
                    pj = json.loads(message)
                    message = CryptoRequest(**pj)
                    logging.debug(message.command)
                    
            
                    if message.command == "start":
                        #check if symbol for binance is in the list and start corountine with binance streaming
                        if message.symbol in settings.binance_symbols:
                            start_task:aio.Task = loop.create_task(bc.start_stream(data_q, message.symbol), name=message.symbol)
                            tasks[message.symbol] = start_task
                        
                        logging.info(" start")
                    
                    if message.command == "stop":
                        stop_task:aio.Task = tasks.get(message.symbol)
                        if stop_task is not None:
                            stop_task.cancel()
                        logging.info(" stop")
        except:
            # kill all binance streaming crountines  when ws client connection was lost or something else goes wrong
            for task in tasks.values():
                task.cancel()
            

    
    async def controller(self)->None:
        
        data_q: aio.Queue = aio.Queue(100)
        tasks: List[aio.Task] = []
        loop = aio.get_event_loop()
        tasks.append(aio.create_task(self.commander(data_q, loop)))
        tasks.append(aio.create_task(self.receive(data_q)))
        aio.run(await aio.gather(*tasks, loop=loop))

        

