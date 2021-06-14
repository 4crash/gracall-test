import asyncio
from asyncio.events import AbstractEventLoop
from asyncio.queues import Queue
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
                                  DataType, 
                                  MessageType,
                                  WsMessage)



class WSServer:
    """ Start ws server and receiving requests from the client.
        Start binance data listening and sending them to the client.
    """
    def __init__(self, websocket:WebSocket):
        self.websocket = websocket
        self.bc = BinanceClient()
        self.tasks: Dict[str, asyncio.Task] = {}
        
        
    
    async def receive_and_send_binance(self, queue: asyncio.Queue)->None:
        """Receive data from binance exchange and send them to client
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
                    res_data = WsMessage(type=MessageType.data,
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
        """Receive data from binance exchange and send them to client

        Args:
            queue (asyncio.Queue): listen for messages from binance data 
        """
        pl:PostLogicAbstr = PostLogic()
        while True:
            posts = pl.get_posts(skip=0, limit=10)
            if len(posts) > 0:
                res_data = WsMessage(type=MessageType.data,
                                         desc=DataType.post,
                                         data=json.dumps([{"title":row.title,
                                                           "author": row.author, 
                                                           "created_at": row.created_at.isoformat()} for row in posts])
                                         )
                await self.websocket.send_json(json.dumps(dataclasses.asdict(res_data)))
            
            await asyncio.sleep(5)
              
                    

    async def command_router(self,queue:asyncio.Queue)->None:
        """ Listen what client's request is and do the appropriate action

        Args:
            data_q (asyncio.Queue): Queue for listening data from binance corountine 
            loop (asyncio.AbstractEventLoop): corountine loop for adding tasks to it by client crypto symbol
        """
        
        await self.websocket.accept()        
        try:
            while True:
                data = await self.websocket.receive()
               
                message = data.get("text")
                if message is not None:
                    # get request in json
                    request = json.loads(message)
                    # parse it to more readable structure 
                    message = WsMessage(**request)
                    logging.debug(message.desc)
                    
                    if message.type == MessageType.binance_command:
                        self.process_binance_command(message=message,queue=queue)
                       
        except:
            # kill all binance streaming tasks when WSclient connection was lost or something else goes wrong
            for task in self.tasks.values():
                task.cancel()
            
            
    def process_binance_command(self, message:WsMessage, queue:Queue):
        """ Start or stop coroutine with binance streaming data

        Args:
            message (WsMessage): parsed message from client
            queue (Queue): queue messages between wsServer and binance croutines
        """
        # check if symbol exists
        if message.symbol in settings.binance_symbols:
            # start task with binance streaming
            if message.desc == ClientCommand.start:
                # check if symbol for binance is in the list and start new task with binance streaming
                start_task: asyncio.Task = self.loop.create_task(self.bc.start_stream(queue, 
                                                                                    message.symbol),
                                                                                    name=message.symbol)
                self.tasks[message.symbol] = start_task
                logging.info("start streaming from binance")
                
            # stop task with binance streaming
            if message.desc == ClientCommand.stop:
                stop_task:Optional[asyncio.Task] = self.tasks.get(message.symbol)
                if stop_task is not None:
                    stop_task.cancel()
                logging.info("stop streaming from binance")
        
    
    async def controller(self)->None:
        """Starts resolver with connection acceptation and select action by commands from client.
            Read what kind of data client require and start/stop new corountine with connection to binance 
        """
        #set messages for data
        queue: asyncio.Queue = asyncio.Queue(100)
        tasks: List[asyncio.Task] = []
        self.loop:AbstractEventLoop = asyncio.get_event_loop()
        # receiving and start listenening commands task
        tasks.append(asyncio.create_task(self.command_router(queue)))
        # receiving data from binance module
        tasks.append(asyncio.create_task(self.receive_and_send_binance(queue)))
        # iterating over time period and check last n posts in database 
        tasks.append(asyncio.create_task(self.receive_and_send_posts()))
        # gather asincio tasks and run
        asyncio.run(await asyncio.gather(*tasks, loop=self.loop))

        

