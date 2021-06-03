from posts.post_logic_router import PostLogic
import uvicorn
from datetime import datetime
from fastapi import FastAPI, HTTPException, WebSocket
from typing import Optional
from fastapi.responses import HTMLResponse
from pydantic_lib.pydantic_post import PostBase, PostDictT, PostOut
from starlette_graphene3 import GraphQLApp
import graphene
from graphql_lib.post_queries import Query
from graphql_lib.post_mutations import Mutation
from html_lib.load_html import load_html
from ws_lib.servant import WSServant
import logging
from settings import settings

# import by settings
logging.basicConfig(level=settings.debug_level)
logging.getLogger("asyncio").setLevel(settings.debug_level)
post_logic = PostLogic()
app = FastAPI()

# async database queries not finished yet
# @app.on_event("startup")
# async def startup():
#     await connect.database.connect()


# @app.on_event("shutdown")
# async def shutdown():
#     await connect.database.disconnect()

# Root page
@app.get("/")
async def root() -> HTMLResponse:
    return HTMLResponse(load_html("main.html"))


# websocket test app
@app.get("/wsapp/")
async def ws_app() -> HTMLResponse:
    return HTMLResponse(load_html("ws.html"))


# WebSocket
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    ws = WSServant(websocket)
    await ws.controller()


# GraphQL
# context_value for proper dependenxy injection model
app.add_route("/graphql/",
              GraphQLApp(schema=graphene.Schema(query=Query, 
                                                mutation=Mutation),
                         context_value={"post_logic": post_logic}))


# REST
@app.post("/posts/", response_model=PostOut)
async def create(post: PostBase) -> PostOut:
    
    new_post = post_logic.create(post)
   
    if new_post is not None:
        return new_post
    else:
        raise HTTPException(status_code=409, 
                            detail="Item hasn't been created, " 
                            "please try it again later.")


@app.put("/posts/{id}/", response_model=PostOut)
async def update(id: int, post: PostOut) -> PostOut:
    edited_post = post_logic.update(post, id)
    if edited_post is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    return edited_post


@app.delete("/posts/{id}/", response_model=PostOut)
async def delete(id: int) -> PostOut:
    del_post = None
    if id is not None:
        del_post = post_logic.delete(id)
    if del_post is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    return del_post


@app.delete("/posts/")
async def delete_all():
    post_logic.reset_posts()


@app.get("/posts/{id}/", response_model=PostOut)
async def detail(id: int) -> PostOut:
    post = post_logic.get_post(id)
    if post is None:
        raise HTTPException(status_code=404, detail="Item not found")

    return post


@app.get("/posts/", response_model=PostDictT)
async def posts(date_from: Optional[datetime] = None, 
                skip: int = 0, 
                limit: int = 20) -> PostDictT:

    if date_from is not None and date_from.tzinfo is None:
        raise HTTPException(
            status_code=400, detail="there is no TimeZone in date_from")
    
    posts = post_logic.get_posts(date_from, skip, limit)
    # print("PPOSTSSSS")
    # print(posts)
    return posts


if __name__ == "__main__":
    uvicorn.run("main:app", 
                host="0.0.0.0", 
                port=8000, 
                reload=True, 
                access_log=False)
