from flask import jsonify, Blueprint
from flask_cors import CORS
from gitlab.stable_deploy.utils import StableDeploy
import json
from requests.exceptions import HTTPError
import os
from gitlab.data.user import User
from gitlab.stable_deploy.error_messages import UNAUTHORIZED, NOT_FOUND

stable_deploy_blueprint = Blueprint("stable_deploy", __name__)
CORS(stable_deploy_blueprint)
GITLAB_API_TOKEN = os.getenv("GITLAB_API_TOKEN", "")


@stable_deploy_blueprint.route("/stable_deploy/ping", methods=["GET"])
def ping_pong():
    return jsonify({
        "status": "success",
        "message": "pong!"
    }), 200


@stable_deploy_blueprint.route("/stable_deploy/<chat_id>",
                               methods=["GET"])
def stable_deploy(chat_id):
    try:
        user = User.objects(chat_id=chat_id).first()
        project = user.project
        stable_deploy = StableDeploy(GITLAB_API_TOKEN)
        pipeline_id = stable_deploy.find_latest_stable_version(project.
                                                               project_id)
        deploy_status = stable_deploy.run_stable_deploy(project.project_id,
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
            deploy_status
        ), 200
