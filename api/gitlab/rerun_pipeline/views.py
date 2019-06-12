from flask import jsonify, Blueprint
from flask_cors import CORS
from gitlab.rerun_pipeline.utils import RerunPipeline
from requests.exceptions import HTTPError
from gitlab.data.user import User
from gitlab.report.error_messages import NOT_FOUND


rerun_pipeline_blueprint = Blueprint("rerun_pipeline", __name__)
CORS(rerun_pipeline_blueprint)


@rerun_pipeline_blueprint.route("/rerun_pipeline/<chat_id>/<pipeline_id>",
                                methods=["GET"])
def rerun_pipeline(chat_id, pipeline_id):
    try:
        user = User.objects(chat_id=chat_id).first()
        project = user.get_user_project()
        rerunpipeline = RerunPipeline(chat_id)
        restarted_pipeline = rerunpipeline.rerun_pipeline(project.project_id,
                                                          pipeline_id)
    except HTTPError as http_error:
        return rerunpipeline.error_message(http_error)
    except AttributeError:
        return jsonify(NOT_FOUND), 404
    else:
        return jsonify(
            restarted_pipeline
        ), 200
