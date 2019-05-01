from flask import jsonify, Blueprint
from flask_cors import CORS
from gitlab.build.utils import Build
from gitlab.build.error_messages import NOT_FOUND, UNAUTHORIZED
from gitlab.data.user import User
from gitlab.data.project import Project
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


@build_blueprint.route("/build/<chat_id>", methods=["GET"])
def get_project_build(chat_id):
    try:
        user = User.objects(chat_id=chat_id).first()
        project = user.project
        project = Project.objects(id=project.id).first()
        if project:
            build = Build(GITLAB_API_TOKEN)
            requested_build = build.get_project_build(project.project_id)
        else:
            dict_error = {"status_code": 404}
            raise HTTPError(json.dumps(dict_error))
    except HTTPError as http_error:
        dict_message = json.loads(str(http_error))
        if dict_message["status_code"] == 401:
            return jsonify(UNAUTHORIZED), 401
        else:
            return jsonify(NOT_FOUND), 404
    except AttributeError:
        return jsonify(NOT_FOUND), 404
    else:
        return jsonify(
            requested_build
        ), 200
