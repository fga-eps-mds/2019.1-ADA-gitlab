# api/gitlab/__init__.py
from requests.exceptions import HTTPError
from requests import get
import json
from flask import jsonify
from gitlab.utils.error_messages import UNAUTHORIZED,\
                                        NOT_FOUND
from gitlab.data.user import User
import re
import sys


class GitlabUtils:
    def __init__(self, chat_id):
        self.chat_id = chat_id
        self.GITLAB_API_TOKEN = self.get_access_token(self.chat_id)
        self.headers = {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + str(self.GITLAB_API_TOKEN)
            }
        self.GITLAB_API_URL = "https://gitlab.com/api/v4/"

    def get_access_token(self, chat_id):
        user = User.objects(chat_id=chat_id).first()
        return user.access_token

    def get_project_id(self, project_owner, project_name):
        project_url = project_owner + "%2F" + project_name
        url = self.GITLAB_API_URL + "projects/{project_url}".format(
              project_url=project_url)
        project_id = self.get_request(url)
        return project_id["id"]

    def error_message(self, http_error):
        dict_message = json.loads(str(http_error))
        if dict_message["status_code"] == 401:
            return jsonify(UNAUTHORIZED), 401
        else:
            return jsonify(NOT_FOUND), 404

    def return_project(self, chat_id,
                       check_project_exists,
                       object_type):
        user = User.objects(chat_id=chat_id).first()
        project = user.get_user_project()
        try:
            if self.get_class_type(object_type) == "Report":
                util = self.check_project_exists(project,
                                                 object_type,
                                                 user)
            else:
                util = self.check_project_exists(project,
                                                 object_type,
                                                 None)
        except HTTPError as http_error:
            raise HTTPError(self.exception_json(http_error.
                                                response.
                                                status_code))
        else:
            return util

    def check_project_exists(self, project, object_type, user=None):
        class_type = self.get_class_type(object_type)
        if class_type == "Pipeline":
            if project:
                util = self.get_project_pipeline(project.project_id)
            else:
                raise HTTPError(self.exception_json(404))
            return util
        elif class_type == "Build":
            if project:
                util = self.get_project_build(project.project_id)
            else:
                raise HTTPError(self.exception_json(404))
        elif class_type == "Report":
            if project:
                util = self.get_project(user.gitlab_user, project.name)
            else:
                raise HTTPError(self.exception_json(404))
        elif class_type == "ReportBranches":
            if project:
                util = self.get_branches(project.project_id)
            else:
                raise HTTPError(self.exception_json(404))
        elif class_type == "ReportCommits":
            if project:
                util = self.get_commits(project.project_id)
            else:
                raise HTTPError(self.exception_json(404))
        elif class_type == "ReportPipelines":
            if project:
                util = self.get_pipeline(project.project_id)
            else:
                raise HTTPError(self.exception_json(404))

        return util

    def get_class_type(self, object):
        raw_class_name = str(type(object)).split('.')[-1]
        class_name = re.sub('[^a-zA-Z]+', '', raw_class_name)
        return class_name

    def get_request(self, url):
        try:
            response = get(url, headers=self.headers)
            response.raise_for_status()
        except HTTPError as http_error:
            raise HTTPError(self.exception_json(http_error.
                                                response.
                                                status_code))
        except AttributeError:
            raise AttributeError(self.exception_json(404))
        except IndexError:
            raise IndexError(self.exception_json(404))
        else:
            resp_json = response.json()
            return resp_json

    def exception_json(self, message):
        error_dict = {"status_code": message}
        return json.dumps(error_dict)
