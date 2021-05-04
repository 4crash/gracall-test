from datetime import datetime
from post import Post
from starlette.testclient import TestClient
from main import app
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
import pytest

post = Post(title="Test", 
            author="edgar",
                  content="lorem ipsum test", 
                  published=True, 
                  published_at=datetime.now().replace(second=0, microsecond=0),
                created_at=datetime.now().replace(second=0, microsecond=0))

def test_root():
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Hello, this is the test blog app for GraCall"}


def test_create_item():
    client = TestClient(app)
    # print(jsonable_encoder(post))
    response = client.post(
        "/create-post/",
        json = jsonable_encoder(post)

    )
    post.id = 1
    assert response.status_code == 200
    assert response.json() == jsonable_encoder(post)


def test_detail():
    client = TestClient(app)
    #create post at first
    response = client.post(
        "/create-post/",
        json=jsonable_encoder(post)

    )
    
    
    post.id = 1
    response = client.get(
        "/get-post/1/"
    )
    
    assert response.status_code == 200
    assert response.json() == jsonable_encoder(post)

    # check not found option
    post.id = -333
    response = client.get(
        "/get-post/66666666"

    )
    assert response.status_code == 404


def test_edit():
    client = TestClient(app)
    #create post at first
    response = client.post(
        "/create-post/",
        json=jsonable_encoder(post)

    )

        
    #set ID of already created post with ID 1 in previous test
    post.id = 1
    response = client.put(
        "/edit-post/",
        json=jsonable_encoder(post)

    )
    
    assert response.status_code == 200
    assert response.json() == jsonable_encoder(post)
    
    # check not found option
    post.id = -333
    response = client.put(
        "/edit-post/",
        json=jsonable_encoder(post)

    )
    assert response.status_code == 404


def test_delete():
    client = TestClient(app)
    post.id = 1
    
    response = client.delete(
        ''.join(["/delete-post/",str(post.id), "/"])

    )
    
    assert response.status_code == 200
    assert response.json() == jsonable_encoder(post)

    # check not found option
    response = client.delete(
        "/delete-post/-555/"

    )
    assert response.status_code == 404


def test_posts():
    # cannot be called alone, it needs to be created post first
    client = TestClient(app)
    response = client.get(
        "/get-posts/"
    )

    assert response.status_code == 200

  
def test_posts_by_date():
    # cannot be called alone, it needs to be created post first
    client = TestClient(app)
    response = client.get(
        "/get-posts/"
    )

    assert response.status_code == 200
