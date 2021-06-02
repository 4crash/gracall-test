from typing import Optional
from datetime import datetime
from pydantic_lib.pydantic_post import PostBase, PostDictT, PostOut
from abc import ABC, abstractclassmethod

class PostLogicAbstr(ABC):
    """ 
        Class for CRUD operations with Blog Posts
    """
    @abstractclassmethod
    def __init__(self) -> None:
        self._posts: PostDictT

    @abstractclassmethod
    def create(self, post: PostBase) -> PostOut:
        """insert post into posts array

        Args:
            post (Post): inserted post

        Returns:
            int: post index
        """
        
        pass

    @abstractclassmethod
    def delete(self, id:int) -> Optional[PostOut]:
        """Delete post with specific id from list

        Args:
            idx (int): post id

        Returns:
            Optional[Post]: deleted post, if exists else None
        """
        pass

    @abstractclassmethod
    def update(self, new_post:PostOut, id:int)->Optional[PostOut]:
        """ Edit specific post

        Args:
            new_post (Post): new_post

        Returns:
            Optional[Post]: new post
        """
        pass

    @abstractclassmethod
    def get_all_posts(self) -> PostDictT:
        """Return all non filtered posts

        Returns:
            List[Post]: posts list
        """
        pass

    @abstractclassmethod
    def get_posts(self, date_from: datetime, skip: int, limit: int) -> PostDictT:
        """ Return posts list with published parameter set to True

        Returns:
            List[Post]: published posts list
        """
        pass


    @abstractclassmethod    
    def get_post(self, id:int)->Optional[PostOut]:
        """ Return specific post by id

        Args:
            idx (int): post id

        Returns:
            Optional[Post]: specific post
        """
        pass
        
    
    def _get_new_index(self) -> int:
        """ return the last index from post list

        Returns:
            [type]: max index 
        """
        pass


    @abstractclassmethod
    def reset_posts(self)->None:
        """Remove all items from the list
        """
        pass 
        

