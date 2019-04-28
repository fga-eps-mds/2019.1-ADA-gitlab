from flask import Blueprint, request, jsonify
from flask_cors import CORS
import os
import sys
from gitlab.data.user import User

webhook_blueprint = Blueprint("webhook", __name__)
CORS(webhook_blueprint)
GITLAB_API_TOKEN = os.getenv("GITLAB_API_TOKEN", "")


@webhook_blueprint.route("/webhook/<userid>/<projectid>",
                         methods=["POST", "GET"])
def webhook_repository(userid, projectid):
    if request.is_json:
        content = request.get_json()
        if content['object_kind'] == "pipeline":
            print('Chegou um pipeline', file=sys.stderr)
            print(content, file=sys.stderr)
            return 'OK'
    else:
        return "JSON Only"


@webhook_blueprint.route("/webhooks/user", methods=["POST"])
def register_user():
    user_data = request.get_json()
    user = User()
    gitlab_user = user_data["gitlab_user"]
    chat_id = user_data["chat_id"]
    gitlab_user_id = user_data["gitlab_user_id"]
    user.save_gitlab_user_data(user, gitlab_user, chat_id, gitlab_user_id)
    return jsonify({
        "status": "OK"
    }), 200


@webhook_blueprint.route("/webhooks/repo", methods=["POST"])
def register_repository():
    repo_data = request.get_json()

    project_name = repo_data["project_name"]
    chat_id = repo_data["chat_id"]
    project_id = repo_data["project_id"]

    user = User.objects(chat_id=chat_id).first()

    user.save_gitlab_repo_data(user, project_name, project_id)
    return jsonify({
        "status": "OK"
    }), 200
