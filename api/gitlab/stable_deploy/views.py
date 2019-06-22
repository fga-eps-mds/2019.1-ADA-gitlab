from flask import jsonify, Blueprint
from flask_cors import CORS
from gitlab.stable_deploy.stable_deploy_utils import StableDeploy
from requests.exceptions import HTTPError
from gitlab.data.user import User
from gitlab.stable_deploy.error_messages import NOT_FOUND


stable_deploy_blueprint = Blueprint("stable_deploy", __name__)
CORS(stable_deploy_blueprint)


@stable_deploy_blueprint.route("/stable_deploy/<chat_id>",
                               methods=["GET"])
def stable_deploy(chat_id):
    try:
        user = User.objects(chat_id=chat_id).first()
        project = user.project
        stable_deploy = StableDeploy(chat_id)
        pipeline_id = stable_deploy.find_latest_stable_version(project.
                                                               project_id)
        deploy_status = stable_deploy.run_stable_deploy(project.project_id,
                                                        pipeline_id)
    except HTTPError as http_error:
        return stable_deploy.error_message(http_error)
    except AttributeError:
        return jsonify(NOT_FOUND), 404
    else:
        return jsonify(
            deploy_status
        ), 200
