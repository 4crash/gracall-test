# Demo-app
- Main libraries: FastAPI, websockets, asyncio, Graphene, Pydantic, SQLALchemy, pytest, mypy, uvicorn
- The App has three connection points REST, GraphQL, Websockets. 
- One Websocket client for downloading binance exchange data 
- One data structure named Post for now.
- Posts can be stored in database or in a list. Switchable in settings. 
- Post has parent abstract class - PostLogicAbstr and two inherited classes  post_logic.PostLogic and post_logic_db.PostLogic
- Websockets are used with asyncio. FrontEnd Client connects to /ws url where Servant class waiting for commands and starts binance asyncio     task for getting streamed prices from binance exchange.
    BinanceClient then sends data over asyncio.queue  back to connected client over Servant.
- Model declara


## Notes
- Please bear in mind that Frontend is not intended for code demonstration. :)
- There is no Docker file. Iam struggling with bluescreen on my computer when  Docker Terminal is launched. (Hope it will be fixed soon)

## TODO
- [ ] Change folders structure
- [x] Test app with postgress DB
- [x] Add live list of added posts to websocket page
- [x] Merge SQlalchemy and pydantic dataModels declaration
- [x] Create solid structure for queuing system , errors, data 
- [ ] Use some kind of vocabulary  for text gathering, language mutations 

## Environment
- python 3.9.x
- sys path for python command 
- pip
- git CLI

## Install steps for Win OS
- Create folder and open it
- Download files from git repository: git clone https://github.com/4crash/gracall-test
- Create virtual environment python -m venv ./venv
- Activate virtual environment  .\venv\Scripts\activate
- Install libraries pip install -r requirements.txt
- Run app with command:  python main.py
- Open http://127.0.0.1:8000/docs in browser for REST
- Open http://127.0.0.1:8000/redoc in browser for REST
- open http://127.0.0.1:8000/wsapp in browser for websockets

## Structure
- Folders
    - db_lib - sqlalchemy ORM files with connection and models
    - graphql_lib - pydantic models, queries and mutations
    - html_lib - simple html files 
    - posts - CRUD logic - post_logic_abstr.py, post_logic.py and post_logic_db
    - pydantic_lib - pydantic models for checking types in rest and graphql  
    - tests - pytests
    - ws_lib - servant.py - web client, binance_client.py - exchange data download

- main.py - url router and starting file
- singleton.py - make singleton from class
- settings.py - app settings
- demo.sqlite - database file

## Tests
- test_post_logic.py - testing post_logic.py it's dependent on settings directive: storage_type 
- test_binance_client.py - test downloading exchange data
- test_post_rest - test rest api
- test_postgraphql - test graphql api
- test_websocket - not finished yet will test websocket server