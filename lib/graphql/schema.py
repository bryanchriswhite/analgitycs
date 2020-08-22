from multiprocessing import cpu_count
from os import environ

import graphene as g

from .queries import RootQuery
from .mutations import RootMutation

# TODO: something else
MAX_WORKERS = cpu_count()


class Labels(g.Enum):
    BRANCH = 0
    TAG = 1
    HASH = 2


schema = g.Schema(query=RootQuery, mutation=RootMutation)
