from typing import List
from pydantic import BaseSettings
import logging

class StorageType:
    DB = "posts.post_logic_db"
    MEMORY = "posts.post_logic"

    

class Settings(BaseSettings):
    # never used yet :)
    app_name: str = "Demo App"

    #binance websocket url
    binance_stream_url:str = "wss://stream.binance.com:9443/ws/{symbol}@depth"

    #allowed symbols from binance
    binance_symbols: List[str] = ["btcusdt", "bnbbtc", "ltcbtc", "ethbtc"]
    
    # sql-lite 
    database_url: str = 'sqlite:///./demo.sqlite'
    
    # postgress
    # database_url: str = 'postgresql://postgres:password@localhost:5432/demo-app'
    
    # logging level
    debug_level: int = logging.WARNING
    
    # saved data into db or into List
    storage_type: str = StorageType.DB


settings = Settings()
