from datetime import datetime
from fastapi import FastAPI, HTTPException
from typing import Any, Dict, List, NamedTuple, Optional
from pydantic import BaseModel
from post import Post
from post_logic import PostLogic
app = FastAPI()
pl = PostLogic()

@app.get("/")
async def root()-> Dict[str,str]:
    return {"message": "Hello, this is the test blog app for GraCall"}

@app.post("/create-post/")
async def create(post: Post) -> Optional[Post]:
    id =  pl.insert(post)
    new_post =  pl.get_post(id)
    return new_post


@app.put("/edit-post/", response_model=Post)
async def edit(post: Post) -> Optional[Post]:
    new_post =  pl.edit(post)
    if new_post is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    return new_post


@app.delete("/delete-post/{id}/", response_model=Post)
async def delete(id: int) -> Optional[Post]:
    del_post = None
    if id is not None:
        del_post =  pl.delete(id)
    if del_post is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    return del_post


@app.get("/get-post/{id}/", response_model=Post)
async def detail(id:int) -> Optional[Post]:
    post =  pl.get_post(id)
    if post is None:
        raise HTTPException(status_code=404, detail="Item not found")

    return post


@app.get("/get-posts-by-date/{datetime}", response_model=List[Post])
async def posts_by_date(date:datetime) -> Optional[List[Post]]:
    posts = pl.get_published_posts_from_date(date)
    
    return posts

@app.get("/get-posts/", response_model=List[Post])
async def posts() -> Optional[List[Post]]:
    posts = pl.get_published_posts()
    
    return posts
