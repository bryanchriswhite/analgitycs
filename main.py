import os
import sys
# import traceback

from flask_api import FlaskAPI, status
from flask_cors import CORS
from flask_graphql import GraphQLView

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lib.blame import BlameManager
from lib.graphql.schema import schema

app = FlaskAPI(__name__)
# app.config['DEFAULT_RENDERERS'] = [
#     'flask_api.renderers.JSONRenderer',
#     'flask_api.renderers.BrowsableAPIRenderer',
# ]
CORS(app,
     supports_credentials=True,
     origins=['http://localhost:8080'])

app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=False))

# Optional, for adding batch query support (used in Apollo-Client)
# app.add_url_rule('/graphql/batch', view_func=GraphQLView.as_view('graphql', schema=schema, batch=True))

# TODO: this should probably be an argument to a track-commit or analysis mutation
# excluded_exts = set()
# ext_whitelist = (
#     ".go", ".proto", ".c", ".h", ".sh", ".md", ".xml", ".wixproj", ".wsx", ".cs"
# )

blame_manager = BlameManager()


@app.errorhandler(500)
def handle_500(error):
    return {'error': 'internal server error'}, status.HTTP_500_INTERNAL_SERVER_ERROR


if __name__ == '__main__':
    app.run()
