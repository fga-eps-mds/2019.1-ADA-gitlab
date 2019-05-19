from flask import jsonify, Blueprint
from flask_cors import CORS
from gitlab.rerun_pipeline.utils import RerunPipeline
import json
from requests.exceptions import HTTPError
import os
from gitlab.data.user import User
from gitlab.report.error_messages import UNAUTHORIZED, NOT_FOUND


rerun_pipeline_blueprint = Blueprint("rerun_pipeline", __name__)
CORS(rerun_pipeline_blueprint)
GITLAB_API_TOKEN = os.getenv("GITLAB_API_TOKEN", "")


@rerun_pipeline_blueprint.route("/rerun_pipeline/ping", methods=["GET"])
def ping_pong():
    return jsonify({
        "status": "success",
        "message": "pong!",
        "route": "rerun_pipeline"
    }), 200


@rerun_pipeline_blueprint.route("/rerun_pipeline/<chat_id>/<pipeline_id>",
                                methods=["GET"])
def rerun_pipeline(chat_id, pipeline_id):
    try:
        user = User.objects(chat_id=chat_id).first()
        project = user.get_user_project()
        rerunpipeline = RerunPipeline(GITLAB_API_TOKEN)
        restarted_pipeline = rerunpipeline.rerun_pipeline(project.project_id,
                                                          pipeline_id)
    except HTTPError as http_error:
        dict_message = json.loads(str(http_error))
        if dict_message["status_code"] == 401:
            return jsonify(UNAUTHORIZED), 401
        else:
            return jsonify(NOT_FOUND), 404
    except AttributeError:
        return jsonify(NOT_FOUND), 404
    else:
        return jsonify(
            restarted_pipeline
        ), 200
