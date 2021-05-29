from typing import Dict, List
from pydantic import BaseSettings
import logging

class StorageType:
    DB = "posts.post_logic_db"
    DICT = "posts.post_logic"

    

class Settings(BaseSettings):
    app_name: str = "Demo App"
    binance_stream_url:str = "wss://stream.binance.com:9443/ws/{symbol}@depth"
    binance_symbols: List[str] = ["btcusdt", "bnbbtc", "ltcbtc", "ethbtc"]
    sqlite_database_url: str = 'sqlite:///./demo.sqlite'
    postgres_database_url: str = 'postgresql://postgres:password@localhost:5432/database'
    debug_level: int = logging.DEBUG
    storage_type:str = StorageType.DB
    #ugly error mesages shoudnt be in settings
    wrong_id_mess: str = 'Post Id doesn\'t exists.'

settings = Settings()
