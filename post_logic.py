from typing import Any, Optional, List
from pydantic import BaseModel
from datetime import date, datetime, tzinfo
# import numpy as np
from post import Post
from singleton import Singleton

class PostLogic(Singleton):
    """ 
        Class for CRUD operations with Blog Posts

    """

    def __init__(self) -> None:
        self.__posts: List[Post] = list()


    def insert(self, post: Post) -> Optional[int]:
        """insert post into posts array

        Args:
            post (Post): inserted post

        Returns:
            int: post index
        """
        
        # simple autoincrement logic
        post.created_at = datetime.now().replace(second=0,microsecond=0)
        post.id = self.get_max_posts_index() + 1
        self.__posts.append(post)
        return post.id

    def delete(self, id:int) -> Optional[Post]:
        """Delete post with specific id from list

        Args:
            idx (int): post id

        Returns:
            Optional[Post]: deleted post, if exists else None
        """
        idx: Optional[int] = self.check_unique_id(id)
        if idx is not None:
            return self.__posts.pop(idx)
        else:
            return None
    
    def edit(self, new_post:Post)->Optional[Post]:
        """ Edit specific post

        Args:
            new_post (Post): new_post

        Returns:
            Optional[Post]: new post
        """
        ind = self.check_unique_id(new_post.id)
        if ind is not None:
            self.__posts[ind] = new_post
            return self.__posts[ind]
        else:
        
            return None
        
    def get_all_posts(self)->List[Post]:
        """Return all non filtered posts

        Returns:
            List[Post]: posts list
        """
        return  self.__posts
    
    def get_published_posts(self) -> List[Post]:
        """ Return posts list with published parameter set to True

        Returns:
            List[Post]: published posts list
        """
        return [row for row in self.__posts if row.published is True]

    def get_published_posts_from_date(self, date:Optional[datetime] = None) -> List[Post]:
        """ get posts published after date param

        Args:
            date (datetime): date_from if it's none then now() is set  

        Returns:
            List[Post]: [description]
        """
        if date is None:
            date = datetime.now()
            
        return [row for row in self.__posts if row.published_at > date]

    def get_post(self, id:Optional[int])->Optional[Post]:
        """ Return specific post by id

        Args:
            idx (int): post id

        Returns:
            Optional[Post]: specific post
        """
        if id is None:
            return None
        
        ind = self.check_unique_id(id)
        
        if ind is not None:
            return self.__posts[ind]
        else:
            return None
        
    def get_max_posts_index(self):
        """ return the last index from post list

        Returns:
            [type]: max index 
        """
        max:int = -1
        if self.__posts is not None and len(self.__posts) > 0:
            for row in self.__posts:
                if row.id > max:
                    max = row.id
            
            return max
                
        else:
            return 0
       
    def check_unique_id(self, id: Optional[int]) -> Optional[int]:
        """ Check if id is not in the list more than once

        Args:
            idx ([type]):checked id

        Raises:
            Exception: if there is more than one same ids

        Returns:
            Optional[int]: return array index 
        """
        output: List[int] = [ind for ind,row in enumerate(
            self.__posts) if row.id == id]
       
        if output is not None and len(output) == 1:
            return output[0]
        elif output is not None and len(output) > 1:
             raise Exception('The post list has multiple rows with the same ID')
        else:
             return None
    
    def reset_posts(self)->None:
        """Reove all items from list
        """
        self.__posts.clear() 
        

