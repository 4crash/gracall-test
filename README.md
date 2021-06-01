# Demo-app demostration of coding skills
- Main libraries: FastAPI, websockets, asyncio, Graphene, Pydantic, SQLALchemy, pytest, mypy
- The App has 3 connection points REST, GraphQL, Websockets and one websocket client for donwloading binance exchange data 
- App has only one data structure named Post, so there's no datamodel relationships for now.
- Posts can be stored in database or in a list. it's switchable in settings. For ccoding demonstration than for real usage. 
- Post has parent abstract class for templating. post_logic_abstr.PostLogicAbstr and two inherited classes from abstract like  post_logic.PostLogic and post_logic_db.PostLogic
- Websockets are used with asyncio. FrontEnd Client connects to /ws url where Servant class waiting for commands and starts binance asyncio task for getting streamed prices for specific symbol from binance exchange.
    BinanceClient then sends data over asyncio.queue  back to connected client over Servant.
- The most of the functionality is covered by tests
- All methods are static typed




## Notes
- Please bear in mind that Frontend is not intended for code demonstration. :)
- There is no Docker file. Iam struggling with bluescreen on my computer when  Docker Terminal is launched. (Hope it will be fixed soon)

## TODO
- Restructuralize folders
- Add more detailed description about app functionalities 
- Try app with postgress DB
- Add live list of added posts to websocket page
- ~~Merge SQlalchemy and pydantic dataModels declaration~~
- Set documented template for queuing system , errors, data 

## Environment
- python 3.9.x
- sys path for python command 
- pip
- git CLI

## How to install and run app :
- This guide is wrote for win OS, please see specific commands manual for your OS system.
- Create folder where the project files will be stored 
- Open the folder
- Download files from git repository git clone https://github.com/4crash/gracall-test
- Create virtual environment python -m venv ./venv
- Activate virtual environment (Windows version) .\venv\Scripts\activate
- Install libraries pip install -r requirements.txt
- Run app with command:  python main.py
- Open http://127.0.0.1:8000/docs in browser for REST
- Open http://127.0.0.1:8000/redoc in browser for REST
- open http://127.0.0.1:8000/wsapp in browser for websockets

## Structure:
- Folders
    - db_lib - sqlalchemy ORM files with connection and mmodels
    - graphql_lib - pydantic models ingerited from pydantic base mmodels , queries and mutations logic
    - html_lib - simple html files 
    - posts - post_logic_abstr parent for post_logic and post_logic_db
    - pydantic_lib - pydantic models for rest and graphql types checking 
    - tests - classic pytests
    - ws_lib - servant.py for web client and binance_client.py for exchange data download

- main.py main file for running app python main.py
- singleton.py 
- settings.py application settings
- demo.sqlite - database file

### Tests ./tests
- test_post_logic.py for testing post_logic.py its dependent on settings directive: storage_type 
- test_binance_client.py test downloading exchange data
- test_post_rest - test rest api
- test_postgraphql - test graphql api
- test_websocket - not finished yet will test websocket server