import os.path as path

import graphene as g
from os import environ
from graphql.error import GraphQLLocatedError
from pyArango.theExceptions import pyArangoException
from pyArango.document import Document
from shutil import rmtree
from typing import List

from lib.git import clone
from lib.util import format_filename
from lib.db import db, REPOS
from .queries import Repo

GIT_ROOT = environ['GIT_ROOT']


# class TrackCommit(g.Mutation):
#     class Arguments:
#         hash = g.String()
#         date = g.DateTime()
#
#     key = g.String()
#     parent_key = g.String()
#     # TODO: Hash type?
#     hash = g.String()
#     commit_date = g.DateTime()
#     committer = g.String()
#     author_date = g.DateTime()
#     author = g.String()
#
#     @staticmethod
#     def mutate(parent, info, commit: CommitInput):
#         print(f'track commit root: {parent}')
#         # TODO: check if commits are already tracked first; if so, only add edges.
#         try:
#             commit = db[COMMITS].createDocument(commit_data)
#             commit.save()
#
#             # TODO: error handling -- `commit['key'] is not None`
#
#             parent_key = commit_data['parent_key']
#             hash = commit_data['hash']
#             if parent_key is not None:
#                 # NB: `[]` uses aragno cache.
#                 parent = db[COMMITS][parent_key]
#                 # TODO: error handling
#                 # NB: `Edge#links` saves the document.
#                 db[CHILD_OF_COMMIT].createDocument({
#                     # TODO:
#                 }).links(parent, commit)
#
#             return TrackCommit(commit)
#         except pyArangoException as e:
#             # TODO:
#             raise e


# class TrackRange(g.Mutation):
#     class Arguments:
#         # TODO: hash type?
#         start_label = g.String()
#         start_type = g.Field(Labels)
#         end_label = g.String()
#         end_type = g.Field(Labels)
#
#     commits = g.List(Commit)
#
#     @staticmethod
#     def mutate(parent, info, commits: g.List[Commit], branch: str = '', range: str = ''):
#         print(f'track range root: {parent}')
#         _commits: List[Commit] = []
#         for commit in commits:
#             result = TrackCommit.mutate(commit, info)
#             # TODO: error handling
#             _commits.append(result.commit)
#
#         return TrackRange(commits=_commits)


class TrackRepo(g.Mutation):
    class Arguments:
        name = g.String()
        url = g.String()

    repo = g.Field(Repo)
    # defaultRange = g.Field(Range)

    @staticmethod
    def mutate(parent, info, name: str, url: str):
        print(f'track repo root: {parent}')
        repo: Document = Document(db[REPOS])
        print(f'repo.modified: {repo.modified}')
        try:
            repo_root = path.join(GIT_ROOT, format_filename(name))
            repo = db[REPOS].createDocument({
                'name': name,
                'url': url,
                'path': repo_root,
            })
            repo.save()
            print(f'repo.modified (saved): {repo.modified}')

            clone(url, repo_root)

            return TrackRepo(repo=repo)
        except (pyArangoException, GraphQLLocatedError, AttributeError) as e:
            # TODO: log/report error
            # NB: document was saved.
            if repo.modified is False:
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
    def mutate(parent, info, key: str):
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
        print(f'root mutation root (parent): {root}')
        return
