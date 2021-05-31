# demo-app
- FastAPI code showcase  

## Notes
- Frontend is easy and functional targeted FE is not main aim of this app
- There is no Docker file. Iam struggling with bluescreen on my computer when  Docker Terminal is launched. (Hope it will be fixed soon)

## TODO
- Add more detailed description about app functi0onalities
- Add check securities from frontend with tokens
- Try app with  postgress DB
- Add live list of added posts to websocket page

## Environment
- python 3.9.x
- sys path for python command 
- pip
- git CLI

## How to install and run app :
- all commands are executed from cmd line on win OS
- create folder where the project files will be stored 
- open the folder
- download files from git repository git clone https://github.com/4crash/gracall-test
- create virtual environment python -m venv ./venv
- activate virtual environment (Windows version) .\venv\Scripts\activate
- install libraries pip install -r requirements.txt
- Run app with command:  python main.py
- open http://127.0.0.1:8000/docs in browser for REST
- open http://127.0.0.1:8000/redoc in browser for REST
- open http://127.0.0.1:8000/wsapp in browser for websockets

## Structure:
- Folders
    - db_lib - sqlalchemy ORM files with connection and mmodels
    - graphql_lib - pydantic models ingerited from pydantic base mmodels , queries and mutations logic
    - html_lib - simple html files 
    - posts - post_log_abstr parent for post_logic and post_logic_db
    - pydantic_lib - pydantic models for rest and graphql type checking 
    - tests - classic pytests
    - ws_lib - servant.py for web client and binance_client.py for exchange data download

- main.py main file for running app python main.py
- singleton.py 
- settings.py application settings
- demo.sqlite - database file

### Tests ./tests
- test_app.py for testing main.py REST api
- test_post_logic.py for testing post_logic.py