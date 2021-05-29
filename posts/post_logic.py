from posts.post_logic_abstr import PostLogicAbstr
from typing import Any, NewType, Optional, Dict, TypeVar
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
        self._posts = PostDictT({}) 


    def create(self, post: PostBase) -> PostOut:
        """insert post into posts array

        Args:
            post (PostBase): inserted post

        Returns:
            PostOut: new post
        """
        new_post_dict = post.dict()
        new_post_dict["id"] = self._get_new_index()
        new_post = PostOut(**new_post_dict)
        
        # new_post.created_at = pytz.utc.localize(
        #     datetime.utcnow().replace(second=0, microsecond=0))
        
        self._posts[new_post.id] = new_post
        return new_post

    def delete(self, id:int) -> Optional[PostOut]:
        """Delete post with specific id from list

        Args:
            idx (int): post id

        Returns:
            Optional[PostOut]: deleted post, if exists else None
        """
        
        return self._posts.pop(id, None)
       
    def update(self, post: PostOut, id: int) -> Optional[PostOut]:
        """ Edit specific post

        Args:
            post (PostOut): post for update

        Returns:
            Optional[PostOut]: updated post
        """
       
        
        # print("ID:  ---- " + str(id))
        if id in self._posts.keys():
            self._posts[id] = post
            return post
        else:
            return None
        
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
        filtered_posts: PostDictT = PostDictT({})
        i:int = 0
        for key in self._posts: 
            if self._posts[key].published is True and \
                (date_from is None or \
                (date_from is not None and self._posts[key].published_at >= date_from)) and \
                i >= skip and i < (skip+limit):
                    
                filtered_posts[key] = self._posts[key]
            i+=1     
        return filtered_posts
    
    
    def get_post(self, id:int)->Optional[PostOut]:
        """ Return specific post by id

        Args:
            idx (int): post id

        Returns:
            Optional[PostOut]: specific post
        """
        # question is if it should return only published post
        return self._posts.get(id)
      
    def _get_new_index(self) -> int:
        """ return the last index from post list

        Returns:
            [type]: max index 
        """
      
        if len(self._posts) > 0:
            # print(self.__posts.keys())
            return max(self._posts.keys())+1
        else:
            return 0
        
   
    def reset_posts(self)->None:
        """Reove all items from list
        """
        self._posts.clear() 
        

post_logic = PostLogic()