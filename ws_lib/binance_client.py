import json
from asyncio import Queue
import asyncio
import websockets 
import logging
from settings import settings
import socket
# from ql_types import OrderSide
# from ql_types.finance import LimitPrice, Quantity

# import qutils.settings as qs

# from orderbook.orderbook import UniqueIdOrderBook
# from binance_app.binance_structs import BinanceSnapshot,BinanceStream



# ob: UniqueIdOrderBook = UniqueIdOrderBook()

# settings = qs.load("dev")
# print(settings)


class BinanceClient:
    """Gets data from binance  
    """
    
       
    async def start_stream(self, q_data: Queue, symbol:str="btcusdt") -> None:
        """ Connect amd receive binance data

        Args:
            q_data (Queue): sending data to
            symbol (str, optional):  specify crytopair symbol  . Defaults to "btcusdt".
        """
        sleep_time = 5
        ping_timeout = 2
        stream_url = settings.binance_stream_url.format(symbol=symbol)
                
        while True:
            try:
                async with websockets.connect(stream_url) as ws:
                    while True:
                        
                        data = await ws.recv()
                        json_l = json.loads(data)
                        await q_data.put(json_l)
                        try:
                            reply = await asyncio.wait_for(ws.recv(), timeout=ping_timeout)
                        except (asyncio.TimeoutError, websockets.exceptions.ConnectionClosed):
                            try:
                                pong = await ws.ping()
                                await asyncio.wait_for(pong, timeout=ping_timeout)
                                logging.debug(
                                    'Ping OK, keeping connection alive...')
                                continue
                            except:
                                await asyncio.sleep(sleep_time)
                                break  # inner loop
                        
            except ConnectionRefusedError:
                # reconnect when failed
                logging.warning("cannot connect to Binance")
                await asyncio.sleep(sleep_time)
                continue
            except socket.gaierror:
                # handling error lost connection in general  
               await q_data.put({'error': 'Binance server connection error'})
               break
               
    
   
