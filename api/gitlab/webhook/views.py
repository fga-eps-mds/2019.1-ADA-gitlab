from flask import Blueprint, request, jsonify
from flask_cors import CORS
import os
import sys
from gitlab.data.user import User
from gitlab.data.project import Project
from gitlab.webhook.utils import Webhook
import json
from requests.exceptions import HTTPError


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
    try:
        webhook = Webhook()
        webhook.register_user(user_data)
    except HTTPError as error:
        dict_message = json.loads(str(error))
        return jsonify(dict_message), 400
    else:
        return jsonify({
            "status": "OK"
        }), 200


@webhook_blueprint.route("/webhooks/repo", methods=["POST"])
def register_repository():
    repo_data = request.get_json()
    try:
        webhook = Webhook()
        webhook.register_repo(repo_data)
    except HTTPError as http_error:
        dict_message = json.loads(str(http_error))
        return jsonify(dict_message), 400
    except AttributeError as attribute_error:
        dict_message = json.loads(str(attribute_error))
        return jsonify(dict_message), 400
    else:
        return jsonify({
            "status": "OK"
        }), 200
