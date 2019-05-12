from flask import jsonify, Blueprint
from flask_cors import CORS
from gitlab.rerun_pipeline.utils import RerunPipeline
import json
from requests.exceptions import HTTPError
import os
from gitlab.data.user import User
from gitlab.data.project import Project
from gitlab.report.error_messages import UNAUTHORIZED, NOT_FOUND


rerun_pipeline_blueprint = Blueprint("rerun_pipeline", __name__)
CORS(rerun_pipeline_blueprint)
GITLAB_API_TOKEN = os.getenv("GITLAB_API_TOKEN", "")


@report_blueprint.route("/rerun_pipeline/ping", methods=["GET"])
def ping_pong():
    return jsonify({
        "status": "success",
        "message": "pong!",
        "route": "rerun_pipeline"
    }), 200


@report_blueprint.route("/rerun_pipeline/<chat_id>", methods=["GET"])
def generate_report(chat_id):
    try:
        user = User.objects(chat_id=chat_id).first()
        project = user.project
        user_has_project = Project.objects(id=project.id)
        if user_has_project:
            restarted_pipeline = RerunPipeline(GITLAB_API_TOKEN)
            # TODO HERE

        else:
            dict_error = {"status_code": 404}
            raise HTTPError(json.dumps(dict_error))

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
            "TODO": "todo"
        ), 200
