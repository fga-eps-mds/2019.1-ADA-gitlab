from flask import jsonify, Blueprint, request, redirect
from flask_cors import CORS
from gitlab.user.utils import UserUtils,\
                              authenticate_access_token,\
                              send_message
from gitlab.user.error_messages import NOT_FOUND
from gitlab.pipeline.views import Pipeline
from gitlab.data.user import User
from requests.exceptions import HTTPError
import os


user_blueprint = Blueprint("user", __name__)
CORS(user_blueprint)
APP_ID = os.getenv("APP_ID", "")
APP_SECRET = os.getenv("APP_SECRET", "")
GITLAB_REDIRECT_URI = os.getenv("REDIRECT_URI", "")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN", "")
BOT_NAME = os.getenv("BOT_NAME", "")


@user_blueprint.route("/user/id/<chat_id>/<project_owner>", methods=["GET"])
def get_user_id(chat_id, project_owner):
    user = UserUtils(chat_id)
    user_id = user.get_user_id(project_owner)
    if not user_id:
        return jsonify(NOT_FOUND), 404
    else:
        return jsonify({
            "user_id": user_id
        }), 200


@user_blueprint.route("/user/repo/<chat_id>/<project_owner>/"
                      "<project_name>",
                      methods=["GET"])
def get_project_id(chat_id, project_owner, project_name):
    try:
        repo = Pipeline(chat_id)
        repo_id = repo.get_project_id(project_owner, project_name)
    except HTTPError as http_error:
        return repo.error_message(http_error)
    else:
        return jsonify({
            "project_id": repo_id
        }), 200


@user_blueprint.route("/user/gitlab/authorize", methods=["GET"])
def get_access_token():
    code = request.args.get('code')
    chat_id = request.args.get('state')
    send_message(ACCESS_TOKEN, chat_id)
    existing_user = User.objects(chat_id=chat_id).first()
    if not existing_user:
        GITLAB_TOKEN = authenticate_access_token(code)
        db_user = User()
        db_user.access_token = GITLAB_TOKEN
        db_user.chat_id = str(chat_id)
        db_user.save()
        user = UserUtils(chat_id)
        user_infos = user.get_own_user_data()
        db_user.gitlab_user = user_infos["gitlab_username"]
        db_user.gitlab_user_id = str(user_infos["gitlab_user_id"])
        db_user.save()
        user.send_button_message(user_infos, chat_id)
    redirect_uri = "https://t.me/{bot_name}".format(bot_name=BOT_NAME)
    return redirect(redirect_uri, code=302)


@user_blueprint.route("/user/domain/<chat_id>", methods=["POST"])
def save_user_domain(chat_id):
    try:
        post_json = request.json
        domain = post_json["domain"]
        user = User.objects(chat_id=chat_id).first()
        user.update(domain=domain)
    except HTTPError as http_error:
        return user.error_message(http_error)
    except AttributeError:
        return jsonify(NOT_FOUND), 404
    else:
        return jsonify({
            "status": "success"
        }), 200


@user_blueprint.route("/user/<chat_id>/domain", methods=["GET"])
def get_user_domain(chat_id):
    try:
        user = UserUtils(chat_id)
        user_domain = user.get_user_domain()
    except AttributeError:
        return jsonify(NOT_FOUND), 404
    else:
        return jsonify({
            "chat_id": chat_id,
            "domain": user_domain
        }), 200


@user_blueprint.route("/user/infos/<chat_id>", methods=["GET"])
def get_user_infos(chat_id):
    dict_user = {"username": 0,
                 "repository": 0}
    user = User.objects(chat_id=chat_id).first()
    if user:
        dict_user["username"] = user.gitlab_user
        dict_user["repository"] = user.project.name
    return jsonify(dict_user), 200
