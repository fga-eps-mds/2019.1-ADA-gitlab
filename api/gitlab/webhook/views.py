from flask import Blueprint, request, jsonify
from flask_cors import CORS
import os
from gitlab.webhook.utils import Webhook
from gitlab.data.user import User
from gitlab.data.project import Project
import json
from requests.exceptions import HTTPError
import telegram
from gitlab.rerun_pipeline.utils import RerunPipeline

webhook_blueprint = Blueprint("webhook", __name__)
CORS(webhook_blueprint)
GITLAB_API_TOKEN = os.getenv("GITLAB_API_TOKEN", "")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN", "")


@webhook_blueprint.route("/webhook/<user_id>/<project_id>",
                         methods=["POST", "GET"])
def webhook_repository(user_id, project_id):
    if request.is_json:
        content = request.get_json()
        if content['object_kind'] == "pipeline":
            webhook = Webhook()
            pipeline_id = content["object_attributes"]["id"]
            jobs = webhook.get_pipeline_infos(project_id, pipeline_id)
            messages = webhook.build_message(jobs)
            status_message = webhook.build_status_message(content,
                                                          jobs)
            project = Project.objects(project_id=project_id).first()
            user = User.objects(project=project.id).first()
            bot = telegram.Bot(token=ACCESS_TOKEN)
            bot.send_message(chat_id=user.chat_id, text=status_message)
            bot.send_message(chat_id=user.chat_id,
                             text=messages["jobs_message"])
            bot.send_message(chat_id=user.chat_id,
                             text=messages["summary_message"])
            if content["object_attributes"]["status"] == "failed" :
                rerunpipeline = RerunPipeline(GITLAB_API_TOKEN)
                botoes = rerunpipeline.build_buttons(pipeline_id)
                bot.send_message(chat_id=user.chat_id,
                                  text=botoes)
            return 'OK'
    else:
        return "OK"


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
