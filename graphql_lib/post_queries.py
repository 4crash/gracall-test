# from pydantic_models import  FinancialModel

import graphene
from graphql_lib.post_models import PostGrapheneOutModel





class Query(graphene.ObjectType):
    
    #definition what will be returned. What type to Graphene list.
    # intro = graphene.String(name=graphene.String(default_value="stranger"))
    posts_list = graphene.List(PostGrapheneOutModel, 
                               skip = graphene.Int(default_value=0), 
                               limit=graphene.Int(default_value = 10),
                               date_from = graphene.DateTime(default_value= None ),
                               )
    post_detail = graphene.Field(
        PostGrapheneOutModel, id=graphene.Int())
 
    
    def resolve_posts_list(parent, info, skip, limit, date_from):
        result =  info.context["post_logic"].get_posts(skip=skip, limit=limit, date_from=date_from)
        return result
    
    def resolve_post_detail(parent, info, id):
        return info.context["post_logic"].get_post(id=id)

    



# schema = graphene.Schema(query=Query, mutation=Mutation)

