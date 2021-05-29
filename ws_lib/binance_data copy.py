
import websockets
import aiohttp
import json
from asyncio import Queue
import asyncio
from typing import Dict
from asyncio import queues
import sys
sys.path.append("../")
# from ql_types import OrderSide
# from ql_types.finance import LimitPrice, Quantity

# import qutils.settings as qs

# from orderbook.orderbook import UniqueIdOrderBook
# from binance_app.binance_structs import BinanceSnapshot,BinanceStream


BINANCE_WSS = "wss://stream.binance.com:9443/ws/{symbol}@depth"
BINANCE_DEPTH_SNAPSHOT = (
    "https://api.binance.com/api/v3/depth?symbol={symbol}&limit=1000"
)
SYMBOLS = ["btcusdt", "bnbbtc"]

# ob: UniqueIdOrderBook = UniqueIdOrderBook()

# settings = qs.load("dev")
# print(settings)


class BinanceClient:
    def __init__(self, symbol: str, snapshot_url: str, stream_url: str) -> None:
        """Not Sure yet what functionalities will be in there :)

        Args:
                symbol (str): symbol for stream
                snapshot_url (str): url for getting snapshot from binance
                stream_url (str): url for getting stream from binance
        """
        self.symbol = symbol
        self.snapshot_url: str = snapshot_url
        self.stream_url: str = stream_url

        self.integrate_symbol()
        self.stream: Dict[int, Dict] = {}
        self.snapshot: Dict = {}
        self.queue: Queue = Queue()

    def integrate_symbol(self) -> None:
        self.snapshot_url = self.snapshot_url.format(
            symbol=self.symbol.upper())
        self.stream_url = self.stream_url.format(symbol=self.symbol.lower())

    async def get_snapshot(self) -> None:
        async with aiohttp.ClientSession() as session:

            async with session.get(self.snapshot_url) as resp:

                while True:
                    if len(self.stream) > 0:
                        response = await resp.json()
                        self.snapshot = response

                # todo check status code
                # if r.status_code == 200:
                #     print(r.text)
                # else:
                #     print(r.status_code)

    async def get_stream(self) -> None:

        async with websockets.connect(self.stream_url) as websocket:
            print("get_stream")
            # todo check status code
            merged: bool = False

            while True:
                # receive
                data = await websocket.recv()
                stream_data = json.loads(data)
                # print(len(self.stream))
                # print(stream_data.get("s"))

                final_id = stream_data.get("u")
                # get snapshot
                # if len(self.snapshot) == 0:
                #     await self.get_snapshot()

                if final_id is not None:
                    self.stream[stream_data.get("u")] = stream_data
                    # self.queue.put(stream_data)
                    # check if stream is continuous
                    # if (
                    #     len(self.stream) > 1
                    #     and self.stream.get(stream_data.get("U") - 1) is None
                    #     and merged is True
                    # ):

                    #     raise ValueError("One or more datastream were lost")

                    # self.stream[stream_data.get("u")] = stream_data
                    # # Throw older stream records
                    # if len(self.snapshot) > 0 and merged is False:
                    #     merged = self.remove_stream_items()
    async def process_stream(self):
        stream = await self.queue.get()
        self.fill_

    def remove_stream_items(self) -> bool:
        merged = False
        for key in list(self.stream):
            if key is not None and key >= self.snapshot["lastUpdateId"]:
                self.stream.pop(key)
                # self.fill_order_book()
                merged = True

        return merged

    # def fill_order_book(self):

    #     for bid in self.snapshot["bids"]:
    #         # print(bid)
    #         if ob.has_order(bid[0], OrderSide.BID) is False:
    #             ob.add_order(
    #                 order_id = str(bid[0]),
    #                 price = LimitPrice(bid[0]),
    #                 quantity = Quantity(bid[1]),
    #                 side = OrderSide.BID,
    #                 position = None,
    #             )

    #     for ask in self.snapshot["asks"]:
    #         if ob.has_order(ask[0], OrderSide.ASK) is False:
    #             ob.add_order(
    #                 order_id = str(ask[0]),
    #                 price = LimitPrice(ask[0]),
    #                 quantity = Quantity(ask[1]),
    #                 side = OrderSide.ASK,
    #                 position = None,
    #             )

        # print(ob)


if __name__ == "__main__":
    for sym in SYMBOLS:
        bc = BinanceClient(sym, BINANCE_DEPTH_SNAPSHOT, BINANCE_WSS)
        asyncio.run(bc.get_stream())
