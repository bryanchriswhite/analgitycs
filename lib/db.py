from os import environ

from pyArango.connection import *

REPOS = 'repos'
COMMITS = 'commits'
FILES = 'files'
collections = [REPOS, COMMITS, FILES]

# TODO: use proper migrations
conn = Connection(
    arangoURL=environ['ARANGO_URL'],
    username=environ['ARANGO_USER'],
    password=environ['ARANGO_PASS']
)

db_name = environ['ARANGO_DB']
db = None

if conn.hasDatabase(db_name):
    db = conn[db_name]
else:
    db = conn.createDatabase(db_name)

for name in collections:
    if not db.hasCollection(name):
        repo_collection = db.createCollection(name=name)
