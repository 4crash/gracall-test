from datetime import datetime, timedelta
from pydantic_lib.pydantic_post import PostBase, PostOut
from posts.post_logic_router import PostLogic
import pytz

pl = PostLogic()
post = PostBase(title="Test", author="edgar",
                  content="lorem ipsum test", published=True, published_at=datetime.now(pytz.utc))
pl.reset_posts()


#fix In real app tests must be runned on the mock tables


def test_create_get_post():
    
    pl.create(post)
    posts = pl.get_all_posts()
    assert posts is not None and len(posts) > 0, "Posts are not filled or get_posts doesnt work"

def test_create_delete_post():
    
    pl.create(post.copy())
    
    posts = pl.get_all_posts()
    before = len(posts)
    
    posts = pl.get_all_posts()
    after = len(posts)
    
    assert int(before) == int(after), "posts were not deleted or not inserted"

def test_get_all_posts():
    pl.reset_posts()
    itr_num = 15
    for i in range(itr_num):
        pl.create(post.copy())
        
    posts = pl.get_all_posts()
    assert len(posts) == itr_num, "number of returned posts is different"


def test_posts_paging():
    pl.reset_posts()
    itr_num = 15
    for i in range(itr_num):
        pl.create(post.copy())
    limit = 10
    skip=3
    posts = pl.get_posts(skip=skip, limit=limit)
    assert len(posts) == limit, "limited returned posts should be different"
    
    skip = 13
    posts = pl.get_posts(skip=skip, limit=limit)
    assert len(posts) == int(itr_num -skip), "skip doesnt work"

def test_get_detail():
    
    pl.create(post.copy())
    post.title = "new title"
    new_post = pl.create(post.copy())
    
    selected_new_post= pl.get_post(new_post.id)
   
    assert selected_new_post.title == post.title, "posts were not the same"


def test_update():
    
    # post insert
    new_title = "changed title"
    post.title = new_title
    new_post:PostOut = pl.create(post.copy())
     
    new_post = pl.update(new_post, new_post.id)
    
    assert new_post is not None, "new post doesnt exists"
    assert new_post.title == new_title, "post was not changed"

def test_get_published_posts_from_date():
    
    pl.reset_posts()
    post.published_at = datetime.now(pytz.utc).replace(
        second=0, microsecond=0) - timedelta(days=5)
    pl.create(post.copy())
    
    post.published_at=datetime.now(pytz.utc).replace(
        second=0, microsecond=0) + timedelta(days=10)
    pl.create(post.copy())
    
    posts = pl.get_posts(datetime.now(pytz.utc).replace(
        second=0, microsecond=0))
    assert len(posts) == 1, "number of returned posts is different"


