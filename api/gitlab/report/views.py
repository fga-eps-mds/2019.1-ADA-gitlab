from flask import jsonify, Blueprint
from flask_cors import CORS
from gitlab.report.utils import Report
from gitlab.report.error_messages import *
import json
from requests.exceptions import HTTPError
import os


report_blueprint = Blueprint("report", __name__)
CORS(report_blueprint)
GITLAB_API_TOKEN = os.getenv("GITLAB_API_TOKEN", "")


@report_blueprint.route("/report/ping", methods=["GET"])
def ping_pong():
    return jsonify({
        "status": "success",
        "message": "pong!"
    }), 200

@report_blueprint.route("/report/<project_owner>/"
                          "<project_name>", methods=["GET"])
def generate_report(project_owner, project_name):
    try:
        report = Report(GITLAB_API_TOKEN)
        generated_report = report.repo_informations(project_owner, project_name)

    except HTTPError as http_error:
        dict_message = json.loads(str(http_error))
        if dict_message["status_code"] == 401:
            return jsonify(UNAUTHORIZED), 401
        else:
            return jsonify(NOT_FOUND), 404

    else:
        return jsonify(
            generated_report
        ), 200      
