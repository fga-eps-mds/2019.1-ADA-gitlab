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
        report = Report(chat_id)
        generated_report = report.return_project(chat_id, 
                                                report.check_project_exists,
                                                report)
    except HTTPError as http_error:
        report.error_message(http_error)
    except AttributeError:
        return jsonify(NOT_FOUND), 404
    else:
        return jsonify(
            generated_report
        ), 200
