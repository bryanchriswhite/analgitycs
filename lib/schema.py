from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED
from multiprocessing import cpu_count
from os import environ, path

import graphene as g
from graphql.error import GraphQLLocatedError
from pyArango.theExceptions import pyArangoException
from pyArango.document import Document
from shutil import rmtree
from typing import List, Dict

from lib.db import db, REPOS, COMMITS, FILES, CHILD_OF_COMMIT
from lib.git import clone
from lib.repo import RepoStat
from lib.util import format_filename, pluck

# TODO: something else
MAX_WORKERS = cpu_count()
GIT_ROOT = environ['GIT_ROOT']


class Author(g.ObjectType):
    name = g.String()
    lines = g.Int()
    additions = g.Int()
    deletions = g.Int()


class File(g.ObjectType):
    authors = g.List(Author)

    length = g.Int()  # Bytes
    name = g.String()


class Commit(g.ObjectType):
    files = g.List(File)

    hash = g.String()
    author = g.String()
    # commiter = g.String()
    message = g.String()
    datetime = g.DateTime()

    @staticmethod
    def resolve_files(parent, info):
        return db[FILES].fetchByExample({'repo': parent._key})


class Range(g.ObjectType):
    # TODO: hash type?
    start = g.String()
    end = g.String()
    commits = g.List(Commit)

    @staticmethod
    def resolve_commits(parent, info):
        raise Exception('not implemented')
        # return db[COMMITS].fetchByExample({'range': parent.range})


class Repo(g.ObjectType):
    ranges = g.List(Range)

    key = g.Int()
    rev = g.String()
    name = g.String()
    url = g.String()

    @staticmethod
    def resolve_key(parent, info):
        return parent['_key']

    @staticmethod
    def resolve_rev(parent, info):
        return parent['_rev']

    @staticmethod
    def resolve_ranges(parent, info):
        raise Exception('not implemented')
        # return db[RANGES].fetchByExample({'repo': parent.repo})


class RootQuery(g.ObjectType):
    repos = g.List(Repo)

    @staticmethod
    def resolve_repos(root, info):
        return db[REPOS].fetchAll()


class TrackCommit(g.Mutation):
    class Arguments:
        hash = g.String()
        date = g.DateTime()

    key = g.String()
    parent_key = g.String()
    # TODO: Hash type?
    hash = g.String()
    commit_date = g.DateTime()
    committer = g.String()
    author_date = g.DateTime()
    author = g.String()

    # file = g.List(File)

    @staticmethod
    def mutate(root, info,
               parent_key: str,
               hash: str,
               author: str,
               author_date: str,
               committer: str,
               commit_date: str,
               ):

        # TODO: check if commits are already tracked first; if so, only add edges.
        try:
            commit_doc = db[COMMITS].createDocument({
                'parent_key': parent_key,
                'hash': hash,
                'author': author,
                'author_date': author_date,
                'committer': committer,
                'committer_date': commit_date
            })
            commit_doc.save()

            # TODO: error handling -- `commit_doc['key'] is not None`
            commit = Commit(
                parent_key=parent_key,
                key=commit_doc['key'],
                hash=hash,
                author=author,
                author_date=author_date,
                committer=committer,
                commit_date=commit_date
            )

            if not parent_key == '':
                # NB: `[]` uses aragno cache
                parent_doc = db[COMMITS][parent_key]
                # TODO: error handling
                db[CHILD_OF_COMMIT].createDocument() \
                    .links(hash, parent_doc, commit_doc)

            return TrackCommit(commit=commit)
        except pyArangoException as e:
            # TODO:
            raise e


class TrackRange(g.Mutation):
    class Arguments:
        # TODO: hash type?
        start = g.String()
        end = g.String()

    commits = g.List(Commit)

    @staticmethod
    def mutate(root, info, commits: List[Dict[str, any]], branch: str = '', range: str = ''):
        _commits: List[Commit] = []
        for commit in commits:
            # args = {k:v for k,v in commit}
            result = TrackCommit.mutate(root, info, **commit)
            # TODO: error handling
            _commit = result.commit
            _commits.append(_commit)
            parent_key = str(_commit.key)

        return TrackRange(commits=_commits)


class TrackRepo(g.Mutation):
    class Arguments:
        name = g.String()
        url = g.String()

    repo = g.Field(Repo)
    defaultRange = g.Field(Range)

    @staticmethod
    def mutate(root, info, name: str, url: str):
        repo: Document = None
        try:
            repo_root = path.join(GIT_ROOT, format_filename(name))
            repo = db[REPOS].createDocument({
                'name': name,
                'url': url,
                'path': repo_root,
            })
            repo.save()

            # TODO: refactor #
            # try:
            clone(url, repo_root)
            # except _ as e:

            rs = RepoStat(name=name, path=repo_root)

            commit_log_pool = ThreadPoolExecutor(MAX_WORKERS)
            commit_fs = rs.commits(commit_log_pool, 'master')
            # TODO: error handling
            [done, _] = wait(commit_fs, return_when=ALL_COMPLETED)
            commits: List[Dict[str, any]] = [{'hash': h, 'date': d} for [h, d] in
                                             [f.result() for f in done if f.result() is not None]]
            ##################

            # NB: track master by default
            default_range = TrackRange.mutate(root, info, commits, branch='master')

            return TrackRepo(repo=repo, defaultRange=default_range)
        except (pyArangoException, GraphQLLocatedError, AttributeError) as e:
            # TODO: log/report error
            if repo is not None:
                # TODO: log/report error
                rmtree(repo.path, ignore_errors=True)
                repo.delete()
            raise e


# TODO: options for order/commit deletion
class DeleteRepo(g.Mutation):
    class Arguments:
        key = g.Int()

    ok = g.Boolean()

    @staticmethod
    def mutate(root, info, key: str):
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


class RootMutation(g.Mutation):
    track_repo = TrackRepo.Field()
    delete_repo = DeleteRepo.Field()

    def mutate(root, info):
        return


schema = g.Schema(query=RootQuery, mutation=RootMutation)
