from flask import jsonify, Blueprint
from flask_cors import CORS
from gitlab.report.report_utils import Report
import json
from requests.exceptions import HTTPError
import os
from gitlab.data.user import User
from gitlab.data.project import Project
from gitlab.report.error_messages import UNAUTHORIZED, NOT_FOUND


report_blueprint = Blueprint("report", __name__)
CORS(report_blueprint)
GITLAB_API_TOKEN = os.getenv("GITLAB_API_TOKEN", "")


@report_blueprint.route("/report/<chat_id>", methods=["GET"])
def generate_report(chat_id):
    try:
        user = User.objects(chat_id=chat_id).first()
        project = user.project
        user_has_project = Project.objects(id=project.id)
        if user_has_project:
            report = Report(GITLAB_API_TOKEN)
            generated_report = report.repo_informations(
                                                        user, project)
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
            generated_report
        ), 200
