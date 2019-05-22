from flask import jsonify, Blueprint
from flask_cors import CORS
from gitlab.build.build_utils import Build
from gitlab.utils.gitlab_utils import GitlabUtils
from gitlab.build.error_messages import NOT_FOUND, UNAUTHORIZED
from gitlab.data.user import User
from gitlab.data.project import Project
import json
from requests.exceptions import HTTPError
import os
import sys

build_blueprint = Blueprint("build", __name__)
CORS(build_blueprint)

@build_blueprint.route("/build/<chat_id>", methods=["GET"])
def get_project_build(chat_id):
    try:
        user = User.objects(chat_id=chat_id).first()
        build = Build(user.access_token)
        user_build = build.return_project(chat_id,
                                          build.check_project_exists,
                                          build)
    except HTTPError as http_error:
        build.error_message(http_error)
    except AttributeError:
        return jsonify(NOT_FOUND), 404
    else:
        return jsonify(
            user_build
        ), 200
