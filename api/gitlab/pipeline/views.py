from flask import jsonify, Blueprint
from flask_cors import CORS
from gitlab.pipeline.pipeline_utils import Pipeline
from requests.exceptions import HTTPError
from gitlab.report.error_messages import NOT_FOUND
import os

pipeline_blueprint = Blueprint("pipeline", __name__)
CORS(pipeline_blueprint)
GITLAB_API_TOKEN = os.getenv("GITLAB_API_TOKEN", "")


@pipeline_blueprint.route("/pipeline/<chat_id>", methods=["GET"])
def get_project_pipeline(chat_id):
    try:
        pipeline = Pipeline(chat_id)
        pipe = pipeline.return_project(chat_id,
                                       pipeline.check_project_exists,
                                       pipeline)
    except HTTPError as http_error:
        pipe.error_message(http_error)
    except AttributeError:
        return jsonify(NOT_FOUND), 404
    else:
        return jsonify({
            "status": pipe["status"],
            "web_url": pipe["web_url"]
        }), 200
