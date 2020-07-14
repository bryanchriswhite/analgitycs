from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED, Future
from graphene import ObjectType, String, Schema, List, Boolean, Field, Mutation, Int, DateTime
from multiprocessing import cpu_count
from os import environ, path
from pyArango.theExceptions import pyArangoException
from pyArango.document import Document
from shutil import rmtree

from lib.db import db, REPOS, COMMITS, FILES
from lib.git import clone
from lib.repo import RepoStat
from lib.util import format_filename

# TODO: something else
MAX_WORKERS = cpu_count()
GIT_ROOT = environ['GIT_ROOT']


class Author(ObjectType):
    name = String()
    lines = Int()
    additions = Int()
    deletions = Int()


class File(ObjectType):
    authors = List(Author)

    length = Int()  # Bytes
    name = String()


class Commit(ObjectType):
    files = List(File)

    hash = String()
    author = String()
    # commiter = String()
    message = String()
    datetime = DateTime()

    @staticmethod
    def resolve_files(parent, info):
        return db[FILES].fetchByExample({'repo': parent._key})


class Repo(ObjectType):
    commits = List(Commit)

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

    @staticmethod
    def resolve_commits(parent, info):
        return db[COMMITS].fetchByExample({'repo': parent._key})


class RootQuery(ObjectType):
    repos = List(Repo)

    @staticmethod
    def resolve_repos(root, info):
        return db[REPOS].fetchAll()


class TrackCommit(Mutation):
    class Arguments:
        hash = String()
        date = DateTime()

    @staticmethod
    def mutate(root, info, hash, date):
        try:
            db[COMMITS].createDocument({
                'hash': hash,
                'date': date
            }).save()
            return TrackCommit()
        except pyArangoException as e:
            # TODO:
            raise e


class TrackRepo(Mutation):
    class Arguments:
        name = String()
        url = String()

    repo = Field(Repo)

    @staticmethod
    def mutate(root, info, name, url):
        repo: Document
        try:
            repo_root = path.join(GIT_ROOT, format_filename(name))
            repo = db[REPOS].createDocument({
                'name': name,
                'url': url,
                'path': repo_root,
            })
            repo.save()

            clone(url, repo_root)
            rs = RepoStat(name=name, path=repo_root)

            commit_log_pool = ThreadPoolExecutor(MAX_WORKERS)
            commit_fs = rs.commits(commit_log_pool, 'master')
            # TODO: error handling
            [done, _] = wait(commit_fs, return_when=ALL_COMPLETED)

            for [hash, date] in [f.result() for f in done if f.result() is not None]:
                TrackCommit.mutate(root, info, hash, date)

            return TrackRepo(repo=repo)
        except pyArangoException as e:
            # TODO: log/report error
            if repo is not None:
                # TODO: log/report error
                rmtree(repo.path, ignore_errors=True)
                repo.delete()
            raise e


# TODO: options for order/commit deletion
class DeleteRepo(Mutation):
    class Arguments:
        key = Int()

    ok = Boolean()

    @staticmethod
    def mutate(root, info, key):
        try:
            repo = db[REPOS][key]
            if repo is None:
                # TODO:
                return DeleteRepo(ok=True)
            rmtree(repo.path, ignore_errors=True)
            repo.delete()
            return True
        except pyArangoException as e:
            # TODO:
            return False


class RootMutation(Mutation):
    track_repo = TrackRepo.Field()
    delete_repo = DeleteRepo.Field()

    def mutate(root, info):
        return


schema = Schema(query=RootQuery, mutation=RootMutation)
