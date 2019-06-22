from flask import jsonify, Blueprint
from flask_cors import CORS
from gitlab.report.report_utils import Report
from requests.exceptions import HTTPError
from gitlab.report.error_messages import NOT_FOUND


report_blueprint = Blueprint("report", __name__)
CORS(report_blueprint)


@report_blueprint.route("/report/<kind>/<chat_id>", methods=["GET"])
def get_data(kind, chat_id):
    try:
        report = Report(chat_id)
        if kind != "project":
            data = report.get_data(kind, chat_id)
        else:
            data = report.return_project(chat_id,
                                         report.check_project_exists,
                                         report)
    except HTTPError as http_error:
        return report.error_message(http_error)
    except AttributeError:
        return jsonify(NOT_FOUND), 404
    else:
        return jsonify(
            data
        ), 200
