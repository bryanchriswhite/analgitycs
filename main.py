import os
import sys
import time
# import traceback
from concurrent.futures import ThreadPoolExecutor, Future
from typing import Any, Dict

from flask import request
from flask_api import FlaskAPI, status
from flask_cors import CORS

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lib import util, error
from lib.blame import BlameManager
from lib.repo import RepoStat
from lib.schema import schema

app = FlaskAPI(__name__)
app.config['DEFAULT_RENDERERS'] = [
    'flask_api.renderers.JSONRenderer',
    'flask_api.renderers.BrowsableAPIRenderer',
]
CORS(app)

repo_stats: Dict[str, RepoStat] = {}

excluded_exts = set()
ext_whitelist = (
    ".go", ".proto", ".c", ".h", ".sh", ".md", ".xml", ".wixproj", ".wsx", ".cs"
)

blame_manager = BlameManager()


@app.route('/graphql')
def handle_graphql():
    result = schema.execute(request.data)

    return {
        'request.data': request.data,
        'result': result
    }


@app.route('/repos')
def handle_repos():
    return repo_stats


@app.errorhandler(500)
def handle_500(error):
    return {'error': 'internal server error'}, status.HTTP_500_INTERNAL_SERVER_ERROR


@app.route('/repo/<string:name>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def handle_repo(name: str):
    if request.method == 'GET':
        try:
            _status = blame_manager.status(name)
            if _status is None:
                return {'msg': f'repo {name} hasn\'t been blamed yet'}
            return _status
        except error.ResponseError as e:
            return e.response()

    if request.data is None:
        return {
                   'error': 'no request params'
               }, status.HTTP_400_BAD_REQUEST

    if request.method == 'POST':
        if name in repo_stats:
            return {'error': 'repo already exists'}, status.HTTP_409_CONFLICT
        path = request.data.pop('path')
        rs = RepoStat(name, path, **request.data)
        print(rs.name)
        print(rs.path)
        print(rs.url)
        blame_manager.add(rs)
        return {
                   'msg': f'repo created',
                   'name': name
               }, status.HTTP_201_CREATED

    if request.method == 'PUT':
        range_ref = request.data.pop('range_ref')
        # ext_whitelist = request.data.pop('ext_whitelist')
        # filter_ext = util.filter_ext(ext_whitelist)
        blame = blame_manager.blame(name, range_ref, **request.data)
        _status = blame.status()
        if not _status['status']['done']:
            return _status, status.HTTP_202_ACCEPTED

        return _status

    if request.method == 'DELETE':
        blame_manager.delete(name)
        return {
            'msg': f'deleted',
            'name': name
        }


if __name__ == '__main__':
    socketio.run(app)
