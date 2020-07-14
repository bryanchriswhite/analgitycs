from os import environ

from pyArango.connection import *
from pyArango.theExceptions import pyArangoException
from graphene import ObjectType, String, Schema, List, Boolean, Field, Mutation, Int

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
    key = Int()
    rev = String()
    name = String()
    url = String()

    @staticmethod
    def resolve_key(parent, info):
        return parent['_key']

    @staticmethod
    def resolve_rev(parent, info):
        return parent['_rev']


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

    @staticmethod
    def mutate(root, info, name, url):
        try:
            repo_collection.createDocument({
                'name': name,
                'url': url
            }).save()
            ok = True
        except pyArangoException as e:
            # TODO: log/report error
            ok = False
        finally:
            return TrackRepo(ok=ok)


class RootMutation(Mutation):
    track_repo = TrackRepo.Field()

    def mutate(root, info):
        return


schema = Schema(query=RootQuery, mutation=RootMutation)
