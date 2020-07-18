from os import environ

from pyArango.connection import *
from pyArango.database import DBHandle as DB

REPOS = 'repos'
RANGES = 'ranges'
COMMITS = 'commits'
FILES = 'files'
CHILD_OF_COMMIT = 'child_of_commit'
collections = [REPOS, RANGES, COMMITS, FILES]
edges = [CHILD_OF_COMMIT]

# TODO: use proper migrations
db: DB
db_name = environ['ARANGO_DB']
conn = Connection(
    arangoURL=environ['ARANGO_URL'],
    username=environ['ARANGO_USER'],
    password=environ['ARANGO_PASS']
)

if conn.hasDatabase(db_name):
    db = conn[db_name]
else:
    db = conn.createDatabase(db_name)

for name in collections:
    if not db.hasCollection(name):
        db.createCollection(name=name)

for name in edges:
    if not db.hasCollection(name):
        db.createCollection(className='Edges', name=name)
