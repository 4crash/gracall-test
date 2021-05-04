from datetime import datetime, timedelta
from pydantic.errors import DateError
import pytest
from post import Post
from post_logic import PostLogic

post = Post(title="Test", author="edgar",
                  content="lorem ipsum test", published=True, published_at=datetime.now())


def test_insert_get_post():
    pl = PostLogic()
    pl.insert(post)
    posts = pl.get_all_posts()
    assert posts is not None and len(posts) > 0, "Posts are not filled or get_posts doesnt work"

def test_insert_delete_post():
    pl = PostLogic()
    pl.insert(post)
    pl.insert(post.copy())
    posts = pl.get_all_posts()
    before = len(posts)
    
    pl.delete(pl.get_max_posts_index())
    posts = pl.get_all_posts()
    
    after = len(posts)
    
    assert int(before-1) == int(after), "posts were not deleted or not inserted"

def test_get_list():
    pl = PostLogic()
    itr_num = 15
    for i in range(itr_num):
        pl.insert(post.copy())
        
    posts = pl.get_all_posts()
    assert len(posts) == itr_num, "number of returned posts is different"


def test_get_detail():
    pl = PostLogic()
    pl.insert(post.copy())
    post.title = "new title"
    new_id = pl.insert(post.copy())
    pl.insert(post.copy())
    selected_post= pl.get_post(new_id)
   
    assert selected_post.title == post.title, "posts were not the same"


def test_edit():
    pl = PostLogic()
    
    new_title = "changed title"
    pid = pl.insert(post.copy())
    old_post = pl.get_post(pid)
    old_post.title = new_title 
    new_post = pl.edit(old_post)
    
    assert new_post is not None, "new post doesnt exists"
    assert new_post.title == new_title, "post was not changed"

def test_get_published_posts_from_date():
    pl = PostLogic()
   
    post.published_at = datetime.now() - timedelta(days=5)
    pl.insert(post.copy())
    post.published_at = datetime.now() + timedelta(days=10)
    pl.insert(post.copy())
    

    posts = pl.get_published_posts_from_date()
    assert len(posts) == 1, "number of returned posts is different"
