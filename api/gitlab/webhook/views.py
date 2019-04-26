from flask import Blueprint, request, jsonify
from flask_cors import CORS
import os
import sys


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


@webhook_blueprint.route("/webhooks", methods=["POST"])
def register_repository():
    user_data = request.get_json()
    return jsonify({
        "sender_id": user_data["sender_id"],
        "gitlab_user": user_data["gitlab_user"],
        "repository": user_data["repository"],
        "repository_id": user_data["repository_id"],
    }), 200
