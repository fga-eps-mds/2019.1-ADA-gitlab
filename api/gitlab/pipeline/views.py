from flask import jsonify, Blueprint
from flask_cors import CORS
from gitlab.pipeline.pipeline_utils import Pipeline
from gitlab.pipeline.error_messages import NOT_FOUND, UNAUTHORIZED
import json
from requests.exceptions import HTTPError
import os
from gitlab.data.user import User
from gitlab.data.project import Project

pipeline_blueprint = Blueprint("pipeline", __name__)
CORS(pipeline_blueprint)
GITLAB_API_TOKEN = os.getenv("GITLAB_API_TOKEN", "")


@pipeline_blueprint.route("/pipeline/ping", methods=["GET"])
def ping_pong():
    return jsonify({
        "status": "success",
        "message": "pong!"
    }), 200


@pipeline_blueprint.route("/pipeline/<chat_id>", methods=["GET"])
def get_project_pipeline(chat_id):
    try:
        user = User.objects(chat_id=chat_id).first()
        pipeline = Pipeline(user.access_token)
        pipe = pipeline.return_project(chat_id,
                                        pipeline.check_project_exists,
                                        True)
    except HTTPError as http_error:
        pipe.error_message(http_error)
    except AttributeError:
        return jsonify(NOT_FOUND), 404
    else:
        return jsonify({
            "status": pipe["status"],
            "web_url": pipe["web_url"]
        }), 200
