from posts.post_logic_abstr import PostLogicAbstr
from typing import Any, List, NewType, Optional, Dict, TypeVar
from pydantic import BaseModel
from datetime import date, datetime, tzinfo
# import numpy as np
from pydantic_lib.pydantic_post import PostBase, PostDictT, PostOut
from singleton import Singleton
import pytz



class PostLogic(Singleton, PostLogicAbstr):
    """ 
        Class for CRUD operations with Blog Posts

    """

    def __init__(self) -> None:
        self._posts = PostDictT([]) 


    def create(self, post: PostBase) -> PostOut:
        """ Create post in list

        Args:
            post (PostBase): inserted post

        Returns:
            PostOut: created post
        """
        # create new dict object
        new_post:Dict = post.dict()
        new_post["id"] = self._get_new_index()
        #convert to postout 
        post_out = PostOut(**new_post)
        self._posts.append(post_out)
        return post_out

    def delete(self, post_id:int) -> Optional[PostOut]:
        """Delete post with specific id from list

        Args:
            post_id (int): post id

        Returns:
            Optional[PostOut]: deleted post, if exists 
        """
        postition = self._get_position(post_id)
        if postition is not None:
            poped_post = self._posts.pop(postition)
            return poped_post
        else:
            return postition
       
    def update(self, post: PostOut, post_id: int) -> Optional[PostOut]:
        """ Edit specific post

        Args:
            post (PostOut): post for update

        Returns:
            Optional[PostOut]: updated post
        """
       
        postition = self._get_position(post_id)
        if postition is not None:
            self._posts[postition] = post
            return self._posts[postition]
        else:
            return postition
      
        
    def get_all_posts(self) -> PostDictT:
        """Return all non filtered posts

        Returns:
            PostDictT: List of Posts with int indexes
        """
        return  self._posts
    
    def get_posts(self, date_from:datetime = None, skip:int = 0,limit:int = 10) -> PostDictT:
        """ Return posts list with published parameter set to True

        Returns:
            List[Post]: published posts list
        """
        filtered_posts: PostDictT = PostDictT([])
        i:int = 0
        for row in self._posts: 
            if row.published is True and \
                (date_from is None or \
                (date_from is not None and row.published_at >= date_from)) and \
                i >= skip and i < (skip+limit):
                    
                filtered_posts.append(row)
            i+=1     
        return filtered_posts
    
    
    def get_post(self, post_id:int)->Optional[PostOut]:
        """ Return specific post by id

        Args:
            idx (int): post id

        Returns:
            Optional[PostOut]: specific post
        """
        # question is if it should return only published post
        postition = self._get_position(post_id)
        if postition is not None:
            return self._posts[postition]
        else:
            return postition
    
    def _get_position(self, post_id:int)->Optional[int]:
        item: Optional[PostOut] = next(
            (row for row in self._posts if row.id == post_id), None)
        if item is not None:
            return self._posts.index(item)
        else:
            return item
    
    def _get_new_index(self) -> int:
        """ return the last index from post list

        Returns:
            [type]: max index 
        """
        first_id = 1
        if self._posts is None:
            self._posts = PostDictT([])
            return first_id
        
        elif len(self._posts) > 0:
            return (self._posts[len(self._posts)-1].id +1)
        
        else:
            return first_id

    def reset_posts(self)->None:
        """Remove all items from list
        """
        self._posts.clear() 
        

post_logic = PostLogic()
