import asyncio as aio
from typing import Dict, List, Optional
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
    

class WSServant:
    """Start ws server and receiving requests from the client.
        Start binance data listening and sending it to the client.
    """
    def __init__(self, websocket:WebSocket):
        self.websocket = websocket
        
        
    
    async def receive_and_send(self, queue: aio.Queue)->None:
        """Receive data from exchange and send them to client

        Args:
            queue (aio.Queue): listen for messages from binance data 
        """
        
        while True:
            data = await queue.get()
            
            if data.get("error"):
                await self.websocket.send_json(data)
                
            else: 
                try:
                    # parse data from binance, data could be missing in some cases, therefore index error
                    binance_json = {
                        "symbol": data["s"],
                        "price": data["b"][0][0],
                        "quantity": data["b"][0][1]
                        
                    }
                    # send result to the client
                    await self.websocket.send_json(binance_json)
                except IndexError as e:
                    # just print warning and check another iteration
                    logging.error("IndexError: " + str(e))
                except KeyError as e:
                    logging.error("Key error: " + str(e))
                except RuntimeError as e:
                    logging.warning("Runtime error: " + str(e))
                     
            
                
            
                    

    async def command_router(self,data_q:aio.Queue, loop:aio.AbstractEventLoop)->None:
        """ Listen what client's request is and do the appropriate action

        Args:
            data_q (aio.Queue): Queue for llistening data from binance corountine 
            loop (aio.AbstractEventLoop): corountine loop for adding tasks to it by client crypto symbol
        """
        
        await self.websocket.accept()
        bc = BinanceClient()
        tasks:Dict[str,aio.Task] = {}
        
        try:
            while True:
                data = await self.websocket.receive()
               
                message = data.get("text")
                if message is not None:
                    # get request in json
                    request = json.loads(message)
                    # parse it to more readable structure 
                    message = CryptoRequest(**request)
                    logging.debug(message.command)
                    
            
                    if message.command == "start":
                        #check if symbol for binance is in the list and start new task with binance streaming
                        if message.symbol in settings.binance_symbols:
                            start_task:aio.Task = loop.create_task(bc.start_stream(data_q, message.symbol), name=message.symbol)
                            tasks[message.symbol] = start_task
                        
                        logging.info(" start")
                    
                    if message.command == "stop":
                        stop_task:Optional[aio.Task] = tasks.get(message.symbol)
                        if stop_task is not None:
                            stop_task.cancel()
                        logging.info(" stop")
        except:
            # kill all binance streaming tasks when ws client connection was lost or something else goes wrong
            for task in tasks.values():
                task.cancel()
            
            

    
    async def controller(self)->None:
        """Starts resolver with connection acceptation and select action by commands from client.
            After that read which data client wants and start new corountine with connection to binance 
            
            Start receive and send dta to client in separated corountine
        """
        #set messages for data
        data_q: aio.Queue = aio.Queue(100)
        tasks: List[aio.Task] = []
        loop = aio.get_event_loop()
        tasks.append(aio.create_task(self.command_router(data_q, loop)))
        tasks.append(aio.create_task(self.receive_and_send(data_q)))
        aio.run(await aio.gather(*tasks, loop=loop))

        

