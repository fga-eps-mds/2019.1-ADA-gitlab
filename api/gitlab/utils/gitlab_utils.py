# api/gitlab/__init__.py

import requests
from requests.exceptions import HTTPError
import json
from flask import jsonify
from gitlab.utils.error_messages import UNAUTHORIZED,\
                                        NOT_FOUND
from gitlab.data.user import User
import requests
import sys


class GitlabUtils:
    def __init__(self, GITLAB_API_TOKEN):
        self.GITLAB_API_TOKEN = GITLAB_API_TOKEN
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
        url = self.GITLAB_API_URL +\
              "projects/{project_url}"\
              .format(project_url=project_url)
        project_id = self.get_request(url)
        return project_id["id"]

    def error_message(self, http_error):
        dict_message = json.loads(str(http_error))
        if dict_message["status_code"] == 401:
            return jsonify(UNAUTHORIZED), 401
        else:
            return jsonify(NOT_FOUND), 404

    def return_project(self, chat_id, check_project_exists, pipeline=True):
        user = User.objects(chat_id=chat_id).first()
        project = user.get_user_project()
        try:
            util = self.check_project_exists(project, pipeline)
        except HTTPError as http_error:
            raise HTTPError(self.exception_json(http_error.
                                                response.
                                                status_code))
        else:
            return util

    def check_project_exists(self, project, pipeline=True):
        if pipeline:
            if project:
                util = self.get_project_pipeline(project.project_id)
            else:
                raise HTTPError(self.exception_json(404))
            return util
        else:
            if project:
                util = self.get_project_build(project.project_id)
            else:
                raise HTTPError(self.exception_json(404))
            return util

    def get_request(self, url):
        try:
            response = requests.get(url, headers=self.headers)
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