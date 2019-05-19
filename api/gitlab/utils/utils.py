# api/gitlab/__init__.py

import requests
from requests.exceptions import HTTPError
import json
from gitlab.pipeline.utils import Pipeline


class GitlabUtils:
    def __init__(self, GITLAB_API_TOKEN):
        self.GITLAB_API_TOKEN = GITLAB_API_TOKEN
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.GITLAB_API_TOKEN
        }

    def get_project_id(self, project_owner, project_name):
        project_url = project_owner + "%2F" + project_name
        try:
            response = requests.get("https://gitlab.com/api/"
                                    "v4/projects/{project_url}"
                                    .format(project_url=project_url),
                                    headers=self.headers)
            response.raise_for_status()
        except HTTPError as http_error:
            dict_error = {"status_code":
                          http_error.response.status_code}
            raise HTTPError(json.dumps(dict_error))
        except AttributeError:
            dict_error = {"status_code": 404}
            raise AttributeError(json.dumps(dict_error))
        else:
            requested_id = response.json()
            return requested_id
    
    def check_project_exists(self, project):
        pass
