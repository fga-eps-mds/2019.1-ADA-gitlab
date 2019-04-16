# api/gitlab/__init__.py

import requests
from requests.exceptions import HTTPError
import json


class Pipeline():
    def __init__(self, GITLAB_API_TOKEN):
        self.GITLAB_API_TOKEN = GITLAB_API_TOKEN

    def get_project_pipeline(self, project_owner, project_name):
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.GITLAB_API_TOKEN
        }
        project_id = self.get_project_id(project_owner, project_name)
        try:
            response = requests.get("https://gitlab.com/api/"
                                    "v4/projects/{project_id}/pipelines"
                                    .format(project_id=project_id["id"]),
                                    headers=headers)
            response.raise_for_status()
        except HTTPError as http_error:
            dict_error = {"status_code": http_error.response.status_code}
            raise HTTPError(json.dumps(dict_error))
        else:
            requested_pipeline = response.json()
            return requested_pipeline[0]

    def get_project_id(self, project_owner, project_name):
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.GITLAB_API_TOKEN
        }
        project_url = project_owner + "%2F" + project_name
        try:
            response = requests.get("https://gitlab.com/api/"
                                    "v4/projects/{project_url}"
                                    .format(project_url=project_url),
                                    headers=headers)
            response.raise_for_status()
        except HTTPError as http_error:
            dict_error = {"status_code": http_error.response.status_code}
            raise HTTPError(json.dumps(dict_error))
        else:
            requested_id = response.json()
            return requested_id