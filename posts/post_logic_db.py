from posts.post_logic_abstr import PostLogicAbstr
from typing import Any, NewType, Optional, Dict, TypeVar
from pydantic import BaseModel
from datetime import date, datetime, tzinfo
# import numpy as np
from pydantic_lib.pydantic_post import PostBase, PostDictT, PostOut
from singleton import Singleton
from db_lib.connect import get_db
from db_lib.post_model import PostModel
from sqlalchemy.orm import Session
from fastapi import Depends
import pytz
from sqlalchemy.sql import select
import logging



class PostLogic(Singleton,PostLogicAbstr):
    """ 
        Class for CRUD operations with Blog Posts

    """
    
    def __init__(self, db:Session = get_db()) -> None:
        self._posts = PostDictT({}) 
        self.db:Session = db


    def create(self, out_post: PostBase,) -> PostOut:
        """insert post into posts array

        Args:
            post (PostBase): inserted post

        Returns:
            PostOut: new post
        """
        
        post = PostModel(**out_post.dict())
        self.db.add(post)
        self.db.commit()
        self.db.refresh(post)
        return PostOut(**post.asdict())

    def delete(self, id:int) -> Optional[PostOut]:
        """Delete post with specific id from list

        Args:
            idx (int): post id

        Returns:
            Optional[PostOut]: deleted post, if exists else None
        """
        
        post = self.db.query(PostModel).get(id)
        if post is not None:
            self.db.delete(post)
            self.db.commit()
        return post
       
    def update(self, new_post: PostOut, id: int) -> Optional[PostOut]:
        """ Edit specific post

        Args:
            post (PostOut): post for update

        Returns:
            Optional[PostOut]: updated post
        """
        
        logging.debug(new_post)
        changed_num:int = self.db.query(PostModel).filter(PostModel.id == id).update(new_post)
        
        if changed_num is not None and changed_num > 0:
            self.db.commit()
            return new_post
        else:
            return None
        
    def get_all_posts(self) -> PostDictT:
        """Return all non filtered posts

        Returns:
            PostDictT: List of Posts with int indexes
        """
        return self.db.query(PostModel).all()
        
    def get_posts(self, date_from: Optional[datetime] = None , skip: int = 0, limit: int = 10) -> PostDictT:
        """ Return posts list with published parameter set to True

        Returns:
            List[Post]: published posts list
        """
        
        if date_from is None:
            date_from = datetime.min.replace(tzinfo=pytz.UTC)
        
       
        
        results = self.db.query(PostModel).filter(PostModel.published == True).filter(
            PostModel.published_at >= date_from).offset(skip).limit(limit).all()

        return results
       
        
    
    def get_post(self, id:int)->Optional[PostOut]:
        """ Return specific post by id

        Args:
            idx (int): post id

        Returns:
            Optional[PostOut]: specific post
        """
        # question is if it should return only published post
        return self.db.query(PostModel).get(id)
            
   
    def reset_posts(self)->None:
        """Remove all items from list
        """
        self.db.query(PostModel).delete()
        

post_logic = PostLogic()
