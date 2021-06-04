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
    binance_command: str = "binance_command"


@dataclass
class WsMessage:
    type: MessageType
    desc: str
    data: Optional[Dict] = None
    symbol: Optional[str] = None

