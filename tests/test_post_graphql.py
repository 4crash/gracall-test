import graphene
from graphene.test import Client
from graphql_lib.post_queries import Query
from graphql_lib.post_mutations import Mutation
from posts.post_logic_router import PostLogic

post_logic = PostLogic()
client = Client(schema=graphene.Schema(
    query=Query, mutation=Mutation), context_value={"post_logic": post_logic})




def test_create_post():
    post_logic.reset_posts()
    author = "me myself and i"
    query = """
        mutation createPost{createPost(post:{
  title:"sdffadfsadfsfasdssd",
  content:"ssfsdfs",
  published: true,
  author: \"""" + author + """\"
  
}){ 
author }}
    """
    result = client.execute(query)

    assert result['data']['createPost']['author'] == author


def test_get_post_list():
    query = """
    query postList{postList(skip:0,limit:10){
        id
        title}},
    """

    result = client.execute(query)
    assert type(result['data']['postList']) == list


def test_get_post():
    query = """
    query {postDetail(id:1){
    id
    author
    }}
    """
    result = client.execute(query)
    assert result['data']['postDetail']['id'] == 1


def test_update_post():
    query = """
    mutation updatePost{updatePost(post:{
        id:1
        title:"new fucking title",
        content:"sdfs",
        published: true,
        author: "jaaa"
        }){
        author}}
    """

    result = client.execute(query)
    assert result['data']['updatePost']['author'] == "jaaa"
    
def test_delete_post():
    query =  """
    mutation deletePost{deletePost(id:1){
        id,
        title}}
    """
    
    result = client.execute(query)
    assert result['data']['deletePost']['id'] == 1



def test_delete_all_posts():
    query = """
    mutation deleteAllPosts{deleteAllPosts}
    """ 
    
    result = client.execute(query)
    assert result['data']['deleteAllPosts'] == True
