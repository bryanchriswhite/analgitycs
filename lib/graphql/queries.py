import graphene as g

from lib.db import db, REPOS, FILES


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
