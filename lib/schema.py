from os import environ

from pyArango.connection import *
from graphene import ObjectType, String, Schema, List, Boolean, Field, Mutation


class Repo(ObjectType):
    name = String()
    url = String


class RootQuery(ObjectType):
    repos = List(Repo)

    @staticmethod
    def resolve_repos(root, info):
        return repo_collection.fetchAll()

# this defines a Field `hello` in our Schema with a single Argument `name`
# hello = String(name=String(default_value="stranger"))
# goodbye = String()

# our Resolver method takes the GraphQL context (root, info) as well as
# Argument (name) for the Field and returns data for the query Response
# def resolve_hello(root, info, name):
#     return f'Hello {name}!'
#
# def resolve_goodbye(root, info):
#     return 'See ya!'


class AddRepo(ObjectType):
    class Arguments:
        name = String()
        url = String()

    ok = Boolean()
    repo = Field(lambda: Repo)


class RootMutation(Mutation):
    add_repo = AddRepo.Field()


schema = Schema(query=RootQuery, muutation=RootMutation)
