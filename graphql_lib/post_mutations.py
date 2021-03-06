from graphql_lib.post_models import (PostGrapheneInputModel,
                                     PostGrapheneOutModel,
                                     PostGrapheneInputIDModel)
from pydantic_lib.pydantic_post import PostBase
import graphene


class CreatePost(graphene.Mutation):
    class Arguments:
        post = PostGrapheneInputModel()

    Output = PostGrapheneOutModel

    @staticmethod
    def mutate(parent, info, post):
        pb = PostBase(**post)
        post = info.context["post_logic"].create(pb)
        return post


class DeletePost(graphene.Mutation):
    class Arguments:
        id = graphene.Int()

    Output = PostGrapheneOutModel

    @staticmethod
    def mutate(parent, info, id):
        post = info.context["post_logic"].delete(id)
        if post is not None:
            return post
        else:
            raise Exception("Item not found")


class DeleteAllPosts(graphene.Mutation):
    Output = graphene.Boolean

    @staticmethod
    def mutate(parent, info):
        info.context["post_logic"].reset_posts()
        return True


class UpdatePost(graphene.Mutation):
    class Arguments:
        post = PostGrapheneInputIDModel()

    Output = PostGrapheneOutModel

    @staticmethod
    def mutate(parent, info, post):
        # pb = PostBase(**post)
        post = info.context["post_logic"].update(post, post.id)
        if post is not None:
            return post
        else:
            raise Exception("Item not found")


class Mutation(graphene.ObjectType):
    create_post = CreatePost.Field()
    delete_post = DeletePost.Field()
    delete_all_posts = DeleteAllPosts.Field()
    update_post = UpdatePost.Field()
