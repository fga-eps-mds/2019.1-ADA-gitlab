from flask import Blueprint, request, jsonify
from flask_cors import CORS
import os
from gitlab.webhook.utils import Webhook
from gitlab.data.user import User
from gitlab.data.project import Project
import json
from requests.exceptions import HTTPError
from telegram import Bot
import telegram
from gitlab.rerun_pipeline.utils import RerunPipeline
from gitlab.webhook.error_messages import NOT_FOUND
from gitlab.user.utils import UserUtils

webhook_blueprint = Blueprint("webhook", __name__)
CORS(webhook_blueprint)
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN", "")


@webhook_blueprint.route("/webhook/<chat_id>/<project_id>",
                         methods=["POST", "GET"])
def webhook_repository(chat_id, project_id):
    if request.is_json:
        content = request.get_json()
        if content["object_kind"] == "pipeline" and "finished_at" in \
           content["object_attributes"]:
            webhook = Webhook(chat_id)
            pipeline_id = content["object_attributes"]["id"]
            jobs = webhook.get_pipeline_infos(project_id, pipeline_id)
            messages = webhook.build_message(jobs)
            status_message = webhook.build_status_message(content,
                                                          jobs)
            project = Project.objects(project_id=project_id).first()
            user = User.objects(project=project.id).first()
            bot = Bot(token=ACCESS_TOKEN)
            if status_message:
                bot.send_message(chat_id=user.chat_id,
                                 text=status_message,
                                 parse_mode='Markdown',
                                 disable_web_page_preview=True)
            if content["object_attributes"]["status"] == "failed":
                rerunpipeline = RerunPipeline(user.chat_id)
                buttons = rerunpipeline.build_buttons(pipeline_id)
                reply_markup = telegram.InlineKeyboardMarkup(buttons)
                bot.send_message(chat_id=user.chat_id,
                                 text=messages["jobs_message"])
                bot.send_message(chat_id=user.chat_id,
                                 text="Se você quiser reiniciar essa pipeline,"
                                      " é só clicar nesse botão",
                                 reply_markup=reply_markup)
            return "OK"
        else:
            return "OK"
    else:
        return "OK"


@webhook_blueprint.route("/webhooks/repo", methods=["POST"])
def register_repository():
    repo_data = request.get_json()
    try:
        chat_id = repo_data["chat_id"]
        webhook = Webhook(chat_id)
        webhook.register_repo(repo_data)
    except HTTPError as http_error:
        dict_message = json.loads(str(http_error))
        return jsonify(dict_message), 400
    except AttributeError:
        return jsonify(NOT_FOUND), 400
    else:
        return jsonify({
            "status": "OK"
        }), 200


@webhook_blueprint.route("/webhook", methods=["POST"])
def set_webhook():
    repo_data = request.get_json()
    try:
        project_id = repo_data["project_id"]
        chat_id = repo_data["chat_id"]
        webhook = Webhook(chat_id)
        webhook.set_webhook(project_id)
    except HTTPError as http_error:
        dict_message = json.loads(str(http_error))
        return jsonify(dict_message), 400
    except AttributeError:
        dict_message = json.dumps(NOT_FOUND)
        return jsonify(dict_message), 400
    else:
        return jsonify({
            "status": "OK"
        }), 200


@webhook_blueprint.route("/user/change_repo_gitlab/<chat_id>", methods=["GET"])
def change_repository_gitlab(chat_id):
    try:
        user = UserUtils(chat_id)
        user_infos = user.get_own_user_data()
        user.send_button_message(user_infos, chat_id)
    except HTTPError as http_error:
        return user.error_message(http_error)
    else:
        return jsonify({
                "status": "OK"
            }), 200
