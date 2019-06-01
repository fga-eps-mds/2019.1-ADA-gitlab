from flask import jsonify, Blueprint, request, redirect
from flask_cors import CORS
from gitlab.user.utils import UserUtils
from gitlab.user.error_messages import NOT_FOUND
from gitlab.pipeline.views import Pipeline
from gitlab.data.user import User
import json
from requests.exceptions import HTTPError
import os
import telegram
import requests

user_blueprint = Blueprint("user", __name__)
CORS(user_blueprint)
GITLAB_API_TOKEN = os.getenv("GITLAB_API_TOKEN", "")
APP_ID = os.getenv("APP_ID", "")
APP_SECRET = os.getenv("APP_SECRET", "")
GITLAB_REDIRECT_URI = os.getenv("REDIRECT_URI", "")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN", "")
BOT_NAME = os.getenv("BOT_NAME", "")


@user_blueprint.route("/user/ping", methods=["GET"])
def ping_pong():
    return jsonify({
        "status": "success",
        "message": "pong!"
    }), 200


@user_blueprint.route("/user/<project_owner>", methods=["GET"])
def get_project_user(project_owner):
    try:
        user = UserUtils(GITLAB_API_TOKEN)
        requested_user = user.get_project_user(project_owner)
        if len(requested_user) == 0:
            return jsonify(NOT_FOUND), 404
    except IndexError:
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
        user = UserUtils(GITLAB_API_TOKEN)
        requested_user_id = user.get_user_id(project_owner)
    except IndexError:
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
        json.loads(str(http_error))
        return jsonify(NOT_FOUND), 404
    except IndexError:
        return jsonify(NOT_FOUND), 404
    else:
        return jsonify({
            "project_id": requested_repo_id["id"]
        }), 200


@user_blueprint.route("/user/gitlab/authorize", methods=["GET"])
def get_access_token():
    code = request.args.get('code')
    chat_id = request.args.get('state')
    header = {"Content-Type": "application/json"}
    redirect_uri = GITLAB_REDIRECT_URI
    data = {
        "client_id": APP_ID,
        "client_secret": APP_SECRET,
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": redirect_uri
    }

    url = "https://gitlab.com/oauth/token"
    data = json.dumps(data)

    try:
        post = requests.post(url=url,
                             headers=header,
                             data=data)
        post_json = post.json()
        GITLAB_TOKEN = post_json['access_token']
        existing_user = User.objects(chat_id=chat_id).first()

        user = UserUtils(GITLAB_TOKEN)
        user_infos = user.get_user()
        if not existing_user:
            db_user = User()
            db_user.access_token = GITLAB_TOKEN
            db_user.chat_id = str(chat_id)
            user = UserUtils(GITLAB_TOKEN)
            user_infos = user.get_user()
            db_user.gitlab_user = user_infos["gitlab_username"]
            db_user.gitlab_user_id = str(user_infos["gitlab_user_id"])
            db_user.save()
        else:
            existing_user.update(access_token=GITLAB_TOKEN)
            user = UserUtils(GITLAB_TOKEN)
            user_infos = user.get_user()
        user.send_message(ACCESS_TOKEN, chat_id)
        redirect_uri = "https://t.me/{bot_name}".format(bot_name=BOT_NAME)
        bot = telegram.Bot(token=ACCESS_TOKEN)
        repo_names = user.select_repos_by_buttons(user_infos
                                                  ["gitlab_username"],
                                                  header)
        reply_markup = telegram.InlineKeyboardMarkup(repo_names)
        bot.send_message(chat_id=chat_id,
                         text="Encontrei esses repositórios na sua "
                         "conta do GitLab. Qual você quer que eu "
                         "monitore? Clica nele!",
                         reply_markup=reply_markup)
    except Exception:
        redirect_uri = "https://t.me/"
    return redirect(redirect_uri, code=302)

@user_blueprint.route("/user/domain/<chat_id>", methods=["POST"])
def save_user_domain(chat_id):
    post_json = request.json
    domain = post_json["domain"]
    user = User.objects(chat_id=chat_id).first()
    user.update(domain=domain)

    return jsonify({
        "status": "success"
    }), 200
