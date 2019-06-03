from flask import jsonify, Blueprint
from flask_cors import CORS
from gitlab.build.build_utils import Build
from gitlab.build.error_messages import NOT_FOUND
from requests.exceptions import HTTPError

build_blueprint = Blueprint("build", __name__)
CORS(build_blueprint)


@build_blueprint.route("/build/<chat_id>", methods=["GET"])
def get_project_build(chat_id):
    try:
        build = Build(chat_id)
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
