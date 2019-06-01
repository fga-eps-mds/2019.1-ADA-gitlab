from flask import jsonify, Blueprint
from flask_cors import CORS
from gitlab.report.report_utils import Report
from requests.exceptions import HTTPError
import os
from gitlab.report.error_messages import NOT_FOUND
from gitlab.report.branch_utils import ReportBranches
from gitlab.report.commit_utils import ReportCommits
from gitlab.report.pipeline_report_utils \
     import ReportPipelines


report_blueprint = Blueprint("report", __name__)
CORS(report_blueprint)
GITLAB_API_TOKEN = os.getenv("GITLAB_API_TOKEN", "")


@report_blueprint.route("/report/branches/<chat_id>", methods=["GET"])
def get_branches(chat_id):
    try:

        branches = ReportBranches(chat_id)
        branches_names = branches.return_project(chat_id,
                                                 branches.check_project_exists,
                                                 branches)
    except HTTPError as http_error:
        branches.error_message(http_error)
    except AttributeError:
        return jsonify(NOT_FOUND), 404
    else:
        return jsonify(
            branches_names
        ), 200


@report_blueprint.route("/report/commits/<chat_id>", methods=["GET"])
def get_commits(chat_id):
    try:
        commits = ReportCommits(chat_id)
        commit_data = commits.return_project(chat_id,
                                             commits.check_project_exists,
                                             commits)
    except HTTPError as http_error:
        return commits.error_message(http_error)
    except AttributeError:
        return jsonify(NOT_FOUND), 404
    else:
        return jsonify(
            commit_data
        ), 200


@report_blueprint.route("/report/pipelines/<chat_id>", methods=["GET"])
def get_pipelines(chat_id):
    try:
        pipeline = ReportPipelines(chat_id)

        pipeline_data = pipeline.return_project(chat_id,
                                                pipeline.check_project_exists,
                                                pipeline)
    except HTTPError as http_error:
        pipeline.error_message(http_error)
    except AttributeError:
        return jsonify(NOT_FOUND), 404
    else:
        return jsonify(
            pipeline_data
        ), 200


@report_blueprint.route("/report/project/<chat_id>", methods=["GET"])
def get_project(chat_id):
    try:

        report = Report(chat_id)

        report_data = report.return_project(chat_id,
                                            report.check_project_exists,
                                            report)
    except HTTPError as http_error:
        report.error_message(http_error)
    except AttributeError:
        return jsonify(NOT_FOUND), 404
    else:
        return jsonify(
            report_data
        ), 200
