
from main import app
from fastapi.testclient import TestClient
client = TestClient(app)

def test_app():
   
    response = client.get('/')
    assert response.status_code == 200

# def test_ws():
#     try:
#         with client.websocket_connect('/ws') as websocket:
#             data = websocket.receive_text()
#             print(data)
#             assert data == 'Hello, world!'
#     except KeyboardInterrupt:
#         print("Canceled")
