# api/gitlab/__init__.py

import requests
from requests.exceptions import HTTPError
import json
import sys


class User():
    def __init__(self, GITLAB_API_TOKEN):
        self.GITLAB_API_TOKEN = GITLAB_API_TOKEN

    def get_project_user(self, project_owner):
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.GITLAB_API_TOKEN
        }
        project_user_id = self.get_project_user_id(project_owner)
        try:
            response = requests.get("https://gitlab.com/api/"
                                    "v4/users/{project_user_id}/projects"
                                    .format(project_user_id=project_user_id[0]["id"]),
                                    headers=headers)
            response.raise_for_status()
        except HTTPError as http_error:
            dict_error = {"status_code": http_error.response.status_code}
            raise HTTPError(json.dumps(dict_error))
        else:
            requested_user = response.json()
            return requested_user

    def get_project_user_id(self, project_owner):
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.GITLAB_API_TOKEN
        }
        try:
            response = requests.get("https://gitlab.com/api/v4/users?username={project_owner}"
                                    .format(project_owner=project_owner),
                                    headers=headers)
            response.raise_for_status()
        except HTTPError as http_error:
            dict_error = {"status_code": http_error.response.status_code}
            raise HTTPError(json.dumps(dict_error))
        else:
            requested_id = response.json()
            return requested_id
