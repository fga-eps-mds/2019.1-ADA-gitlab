from flask import jsonify, Blueprint
from flask_cors import CORS
from gitlab.pipeline.utils import Pipeline
from gitlab.pipeline.error_messages import NOT_FOUND, UNAUTHORIZED
import json
from requests.exceptions import HTTPError
import os


pipeline_blueprint = Blueprint("pipeline", __name__)
CORS(pipeline_blueprint)
GITLAB_API_TOKEN = os.getenv("GITLAB_API_TOKEN", "")


@pipeline_blueprint.route("/pipeline/ping", methods=["GET"])
def ping_pong():
    return jsonify({
        "status": "success",
        "message": "pong!"
    }), 200


@pipeline_blueprint.route("/pipeline/<project_owner>/"
                          "<project_name>", methods=["GET"])
def get_project_pipeline(project_owner, project_name):
    try:
        pipeline = Pipeline(GITLAB_API_TOKEN)
        requested_pipeline = pipeline.get_project_pipeline(project_owner,
                                                           project_name)
    except HTTPError as http_error:
        dict_message = json.loads(str(http_error))
        if dict_message["status_code"] == 401:
            return jsonify(UNAUTHORIZED), 401
        else:
            return jsonify(NOT_FOUND), 404
    else:
        return jsonify({
            "status": requested_pipeline["status"],
            "web_url": requested_pipeline["web_url"]
        }), 200
