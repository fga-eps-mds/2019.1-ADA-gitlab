from flask import jsonify, Blueprint
from flask_cors import CORS
from gitlab.pipeline.utils import Pipeline
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
        project = user.project
        project = Project.objects(id=project.id).first()
        if project:
            pipeline = Pipeline(GITLAB_API_TOKEN)
            pipe = pipeline.get_project_pipeline(project.project_id)
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
        return jsonify({
            "status": pipe["status"],
            "web_url": pipe["web_url"]
        }), 200
