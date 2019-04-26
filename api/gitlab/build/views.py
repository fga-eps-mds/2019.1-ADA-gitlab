from flask import jsonify, Blueprint
from flask_cors import CORS
from gitlab.build.utils import Build
from gitlab.build.error_messages import NOT_FOUND, UNAUTHORIZED
import json
from requests.exceptions import HTTPError
import os


build_blueprint = Blueprint("build", __name__)
CORS(build_blueprint)
GITLAB_API_TOKEN = os.getenv("GITLAB_API_TOKEN", "")


@build_blueprint.route("/build/ping", methods=["GET"])
def ping_pong():
    return jsonify({
        "status": "success",
        "message": "pong!"
    }), 200


@build_blueprint.route("/build/<project_owner>/"
                       "<project_name>", methods=["GET"])
def get_project_build(project_owner, project_name):
    try:
        build = Build(GITLAB_API_TOKEN)
        requested_build = build.get_project_build(project_owner,
                                                  project_name)
    except HTTPError as http_error:
        dict_message = json.loads(str(http_error))
        if dict_message["status_code"] == 401:
            return jsonify(UNAUTHORIZED), 401
        else:
            return jsonify(NOT_FOUND), 404
    else:
        return jsonify(
            requested_build
        ), 200
