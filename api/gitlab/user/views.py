from flask import jsonify, Blueprint
from flask_cors import CORS
from gitlab.user.utils import User
from gitlab.user.error_messages import NOT_FOUND, UNAUTHORIZED
import json
from requests.exceptions import HTTPError
import os


user_blueprint = Blueprint("user", __name__)
CORS(user_blueprint)
GITLAB_API_TOKEN = os.getenv("GITLAB_API_TOKEN", "")


@user_blueprint.route("/user/ping", methods=["GET"])
def ping_pong():
    return jsonify({
        "status": "success",
        "message": "pong!"
    }), 200

@user_blueprint.route("/user/<project_owner>", methods=["GET"])
def get_project_user(project_owner):
    try:
        user = User(GITLAB_API_TOKEN)
        requested_user = user.get_project_user(project_owner)
    except HTTPError as http_error:
        dict_message = json.loads(str(http_error))
        if dict_message["status_code"] == 401:
            return jsonify(UNAUTHORIZED), 401
        else:
            return jsonify(NOT_FOUND), 404
    else:
        return jsonify({
            "repo": requested_user["name"]
        }), 200
