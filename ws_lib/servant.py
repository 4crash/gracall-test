import asyncio
import dataclasses
import logging
from typing import Dict, List, Optional
from ws_lib.binance_client import BinanceClient
import json
from fastapi import WebSocket
from settings import settings
from posts.post_logic_router import PostLogic
from posts.post_logic_abstr import PostLogicAbstr
from ws_lib.message_types import (ClientCommand, 
                                  CryptoRequestData, DataType, 
                                  MessageType,
                                  WsMessageData)



class WSServant:
    """Start ws server and receiving requests from the client.
        Start binance data listening and sending it to the client.
    """
    def __init__(self, websocket:WebSocket):
        self.websocket = websocket
        
        
    
    async def receive_and_send_binance(self, queue: asyncio.Queue)->None:
        """Receive data from exchange and send them to client

        Args:
            queue (asyncio.Queue): listen for messages from binance data 
        """
        
        while True:
            data = await queue.get()
            
            if data.get("error"):
                await self.websocket.send_json(data)
                
            else: 
                try:
                    # parse data from binance, data could be missing in some cases, therefore index error
                    res_data = WsMessageData(type=MessageType.data,
                                             desc= DataType.binance,
                                             data={
                                                 "symbol": data["s"],
                                                 "price": data["b"][0][0],
                                                 "quantity": data["b"][0][1]}
                                             )
                  
                    # send result to the client
                    await self.websocket.send_json(json.dumps(dataclasses.asdict(res_data)))
                                                   
                except IndexError as e:
                    # just print warning and check another iteration
                    logging.error("IndexError: " + str(e))
                except KeyError as e:
                    logging.error("Key error: " + str(e))
                except RuntimeError as e:
                    logging.warning("Runtime error: " + str(e))
                    
    
    async def receive_and_send_posts(self)->None:
        """Receive data from exchange and send them to client

        Args:
            queue (asyncio.Queue): listen for messages from binance data 
        """
        pl:PostLogicAbstr = PostLogic()
        while True:
            posts = pl.get_posts(skip=0, limit=10)
            if len(posts) > 0:
                res_data = WsMessageData(type=MessageType.data,
                                         desc=DataType.post,
                                         data=json.dumps([{"title":row.title,
                                                           "author": row.author, 
                                                           "created_at": row.created_at.isoformat()} for row in posts])
                                         )
                await self.websocket.send_json(json.dumps(dataclasses.asdict(res_data)))
            
            await asyncio.sleep(5)
              
                    

    async def command_router(self,data_q:asyncio.Queue, loop:asyncio.AbstractEventLoop)->None:
        """ Listen what client's request is and do the appropriate action

        Args:
            data_q (asyncio.Queue): Queue for llistening data from binance corountine 
            loop (asyncio.AbstractEventLoop): corountine loop for adding tasks to it by client crypto symbol
        """
        
        await self.websocket.accept()
        bc = BinanceClient()
        tasks:Dict[str,asyncio.Task] = {}
        
        try:
            while True:
                data = await self.websocket.receive()
               
                message = data.get("text")
                if message is not None:
                    # get request in json
                    request = json.loads(message)
                    # parse it to more readable structure 
                    message = CryptoRequestData(**request)
                    logging.debug(message.command)
                    
            
                    if message.command == ClientCommand.start:
                        #check if symbol for binance is in the list and start new task with binance streaming
                        if message.symbol in settings.binance_symbols:
                            start_task:asyncio.Task = loop.create_task(bc.start_stream(data_q, message.symbol), name=message.symbol)
                            tasks[message.symbol] = start_task
                        
                        logging.info("start streaming from binance")
                    
                    if message.command == ClientCommand.stop:
                        stop_task:Optional[asyncio.Task] = tasks.get(message.symbol)
                        if stop_task is not None:
                            stop_task.cancel()
                        logging.info("stop streaming from binance")
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
        data_q: asyncio.Queue = asyncio.Queue(100)
        tasks: List[asyncio.Task] = []
        loop = asyncio.get_event_loop()
        # receiving and start listenening commands task
        tasks.append(asyncio.create_task(self.command_router(data_q, loop)))
        # receiving data from binance module
        tasks.append(asyncio.create_task(self.receive_and_send_binance(data_q)))
        # iterate over time period and check last n posts in database 
        tasks.append(asyncio.create_task(self.receive_and_send_posts()))
        # gather asincio tasks and run
        asyncio.run(await asyncio.gather(*tasks, loop=loop))

        

