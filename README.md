# gracall-test
- FastAPI code showcase for gracall

## Notes
- Theres no Asyncio callings because of no IO operations.

## How to run app:
- pip install -r requirements.txt
- Run app with command:  uvicorn main:app

## Structure:
- main.py with FastAPi REST environment 
- post.py BaseModel for blog posts
- post_logic.py CRUD opertations with Posts list 
- singleton.py for setting class as singleton

### Tests ./tests
- test_app.py for testing main.py REST api
- test_post_logic.py for testing post_logic.py