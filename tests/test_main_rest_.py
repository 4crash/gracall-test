from datetime import datetime, timedelta
from typing import Optional
from pydantic_lib.pydantic_post import PostBase, PostDictT, PostOut
from starlette.testclient import TestClient
from main import app
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
import pytz
import pytest
from urllib import parse

client = TestClient(app)
non_exist_id = -3333
non_exists_url = "/posts/"+str(non_exist_id)+"/"
url = "/posts/"
created_post:Optional[PostOut] = None

post = PostBase(title="Test", 
                author="edgar",
                  content="lorem ipsum test", 
                  published=True, 
                  published_at=datetime.now(pytz.utc).replace(second=0, microsecond=0)
                )

def test_root():
    
    response = client.get("/")
    assert response.status_code == 200
   

@pytest.mark.detail
def test_create_post():
    # print(jsonable_encoder(post))
    response = client.post(
        url,
        json = jsonable_encoder(post)

    )
    
    global created_post
    created_post = PostOut(**response.json())
    
    assert response.status_code == 200
    assert response.json()["title"] == jsonable_encoder(post)["title"]


@pytest.mark.detail
def test_detail():
    
    response = client.get(
       url+str(created_post.id)+"/"
    )
    assert response.status_code == 200
    assert response.json() == jsonable_encoder(created_post)

    # check not found option
    response = client.get(
        non_exists_url

    )
    assert response.status_code == 404


def test_update():
    #create post at first
          
    response = client.put(
        url+str(created_post.id)+"/",
        json=jsonable_encoder(created_post)

    )
    
    assert response.status_code == 200
    assert response.json() == jsonable_encoder(created_post)
    
    # check not found option
    response = client.put(
        non_exists_url,
        json=jsonable_encoder(created_post)

    )
    assert response.status_code == 404


def test_posts():
    # cannot be called alone, it needs to be created post first
    response = client.get(
        url,
        # headers={"X-Token": "testtoken"}
    )

    assert response.status_code == 200, str(response.content)


def test_posts_queries():
    # cannot be called alone, it needs to be created post first
    params = {
        "date_from": (datetime.now(pytz.utc).replace(second=0, microsecond=0)-timedelta(days=1)).isoformat(),
        "skip": 0,
        "limit": 20
    }
    url_path = url + "?" + parse.urlencode(params, doseq=True)
    # url_path = parse.parse_qs(url_path)
    print(url_path)
    response = client.get(
       url_path
    )
    assert response.status_code == 200, response.content
  

def test_delete():

    response = client.delete(
        url+str(created_post.id)+"/"

    )
    assert response.status_code == 200
    assert response.json()["title"] == jsonable_encoder(post)["title"]

    # check not found option
    response = client.delete(
        non_exists_url

    )
    assert response.status_code == 404
    

