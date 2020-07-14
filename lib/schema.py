from os import environ

from pyArango.connection import *
from graphene import ObjectType, String, Schema, List, Boolean, Field, Mutation

# TODO: use proper migrations
conn = Connection(
    arangoURL=environ['ARANGO_URL'],
    username=environ['ARANGO_USER'],
    password=environ['ARANGO_PASS']
)
db_name = environ['ARANGO_DB']
db = None
repo_collection = None

if conn.hasDatabase(db_name):
    db = conn[db_name]
else:
    db = conn.createDatabase(db_name)

if db.hasCollection('repos'):
    repo_collection = db['repos']
else:
    repo_collection = db.createCollection(name='repos')


class Repo(ObjectType):
    name = String()
    url = String()


class RootQuery(ObjectType):
    repos = List(Repo)

    @staticmethod
    def resolve_repos(root, info):
        return repo_collection.fetchAll()


class TrackRepo(Mutation):
    class Arguments:
        name = String()
        url = String()

    ok = Boolean()
    repo = Field(lambda: Repo)

    def mutate(root, info):
        return


class RootMutation(Mutation):
    track_repo = TrackRepo.Field()

    def mutate(root, info):
        return


schema = Schema(query=RootQuery)  # , mutation=RootMutation)
