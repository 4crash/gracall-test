from dataclasses import dataclass
from typing import Dict, Optional

# modul for defining message structure between client, bonance and servant

class DataType:
    binance = "binance"
    post = "post"

class ClientCommand:
    start = "start"
    stop = "stop"


class MessageType:
    error: str = "error"
    data: str = "data"
    warning: str = "warning"
    command: str = ClientCommand


@dataclass
class WsMessageData:
    type: MessageType
    desc: str
    data: Optional[Dict]


@dataclass
class CryptoRequestData:
    symbol: str
    command: str


# @dataclass
# class BinanceData:
#     symbol: str
#     price: str
#     quantity: str
