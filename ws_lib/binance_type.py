from typing import Dict, List, NewType
from pydantic import BaseModel
from datetime import datetime

from pydantic.types import Json

Price = NewType("Price",int)
Quantity = NewType("Quantity", int)

class BinanceResponseT(BaseModel):
    # there is no need to map 'u' 'U' values They are for mapping to snapshots 
    event_type: str
    event_time: datetime
    symbol: str
    bids: List[Dict[Price,Quantity]]
    asks: List[Dict[Price,Quantity]]
    
    # def convert_from_binance_stream(self, data: Json):
    #     self.event_type = str(data["e"])
    #     self.event_time = datetime(data["E"])
    #     self.symbol = data["s"]
    #     self.bids = data["b"]
    #     self.asks = data["a"]
    
    
