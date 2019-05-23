from flask import jsonify, Blueprint, request, redirect
from flask_cors import CORS
from gitlab.user.utils import UserUtils,\
                              authenticate_access_token,\
                              send_message
from gitlab.user.error_messages import NOT_FOUND, UNAUTHORIZED
from gitlab.pipeline.views import Pipeline
from gitlab.data.user import User
import json
from requests.exceptions import HTTPError
import os
import telegram
import requests
import sys

user_blueprint = Blueprint("user", __name__)
CORS(user_blueprint)
GITLAB_API_TOKEN = os.getenv("GITLAB_API_TOKEN", "")
APP_ID = os.getenv("APP_ID", "")
APP_SECRET = os.getenv("APP_SECRET", "")
GITLAB_REDIRECT_URI = os.getenv("REDIRECT_URI", "")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN", "")
BOT_NAME = os.getenv("BOT_NAME", "")


@user_blueprint.route("/user/<project_owner>", methods=["GET"])
def get_user_project(project_owner):
    try:
        user = UserUtils(GITLAB_API_TOKEN)
        user_repos = user.get_user_project(project_owner)
        if len(user_repos) == 0:
            return jsonify(NOT_FOUND), 404
    except HTTPError as http_error:
        user.error_message(http_error)
    except IndexError:
        return jsonify(NOT_FOUND), 404
    else:
        repositories_names = []
        for item in user_repos:
            repositories_names.append(item["path_with_namespace"])
        return jsonify({
            "repositories": repositories_names
        }), 200


@user_blueprint.route("/user/id/<project_owner>", methods=["GET"])
def get_user_id(project_owner):
    try:
        user = UserUtils(GITLAB_API_TOKEN)
        user_id = user.get_user_id(project_owner)
    except HTTPError as http_error:
        user.error_message(http_error)
    else:
        return jsonify({
            "user_id": user_id
        }), 200


@user_blueprint.route("/user/repo/<project_owner>/"
                      "<project_name>",
                      methods=["GET"])
def get_project_id(project_owner, project_name):
    try:
        repo = Pipeline(GITLAB_API_TOKEN)
        repo_id = repo.get_project_id(project_owner, project_name)
    except HTTPError as http_error:
        repo.error_message(http_error)
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
        user = UserUtils(GITLAB_TOKEN)
        user_infos = user.get_own_user_data()
        db_user.gitlab_user = user_infos["gitlab_username"]
        db_user.gitlab_user_id = str(user_infos["gitlab_user_id"])
        db_user.save()    
        user.send_button_message(user_infos, chat_id)
    
    redirect_uri = "https://t.me/{bot_name}".format(bot_name=BOT_NAME)    

    return redirect(redirect_uri, code=302)
