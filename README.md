# gracall-test
- FastAPI code showcase for gracall

## Notes
- Theres no Asyncio callings because of no IO operations.
- Iam sorry that there is no Docker file. Iam struggling with bluescreen on my computer when I run Docker Terminal. (Hope I will fix it soon)

## Environment
- python 3.9.x
- set sys path for python command 
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
- Run app with command:  uvicorn main:app
- open http://127.0.0.1:8000/docs in browser

## Structure:
- main.py with FastAPi REST environment 
- post.py BaseModel for blog posts
- post_logic.py CRUD opertations with Posts list 
- singleton.py for setting class as singleton

### Tests ./tests
- test_app.py for testing main.py REST api
- test_post_logic.py for testing post_logic.py