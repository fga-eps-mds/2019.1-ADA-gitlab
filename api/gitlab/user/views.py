from flask import jsonify, Blueprint
from flask_cors import CORS
from gitlab.user.utils import User
from gitlab.user.error_messages import NOT_FOUND, UNAUTHORIZED
from gitlab.pipeline.views import Pipeline
import json
from requests.exceptions import HTTPError
import os
import sys


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
        if len(requested_user) == 0:
            return jsonify(NOT_FOUND), 404
    except HTTPError as http_error:
        dict_message = json.loads(str(http_error))
        if dict_message["status_code"] == 401:
            return jsonify(UNAUTHORIZED), 401
        else:
            return jsonify(NOT_FOUND), 404
    else:
        repositories_names = []

        for item in requested_user:
            repositories_names.append(item["path_with_namespace"])
        return jsonify({
            "repositories": repositories_names
        }), 200


@user_blueprint.route("/user/id/<project_owner>", methods=["GET"])
def get_user_id(project_owner):
    try:
        user = User(GITLAB_API_TOKEN)
        requested_user_id = user.get_user_id(project_owner)
    except HTTPError as http_error:
        dict_message = json.loads(str(http_error))
        if dict_message["status_code"] == 401:
            return jsonify(UNAUTHORIZED), 401
        else:
            return jsonify(NOT_FOUND), 404
    else:
        return jsonify({
            "user_id": requested_user_id
        }), 200


@user_blueprint.route("/user/repo/<project_owner>/"
                      "<project_name>",
                      methods=["GET"])
def get_project_id(project_owner, project_name):
    try:
        repo = Pipeline(GITLAB_API_TOKEN)
        requested_repo_id = repo.get_project_id(project_owner, project_name)
    except HTTPError as http_error:
        dict_message = json.loads(str(http_error))
        if dict_message["status_code"] == 401:
            return jsonify(UNAUTHORIZED), 401
        else:
            return jsonify(NOT_FOUND), 404
    else:
        return jsonify({
            "project_id": requested_repo_id["id"]
        }), 200