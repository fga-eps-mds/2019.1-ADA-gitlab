# api/gitlab/__init__.py

import requests
from requests.exceptions import HTTPError
import json
from gitlab.pipeline.utils import Pipeline
import sys

class Build():
    def __init__(self, GITLAB_API_TOKEN):
        self.GITLAB_API_TOKEN = GITLAB_API_TOKEN

    def get_project_build(self, project_owner, project_name):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.GITLAB_API_TOKEN
        }
        project_id = self.get_project_id(project_owner, project_name)
        try:
            teste2 = Pipeline(self.GITLAB_API_TOKEN)
            # teste2.get_project_pipeline(project_owner, project_name)
            pipeline_id = teste2.get_project_pipeline(project_owner, project_name)
            response = requests.get("https://gitlab.com/api/"
                                    "v4/projects/{project_id}/pipelines/{pipeline_id}/jobs"
                                    .format(project_id=project_id['id'], pipeline_id=pipeline_id["id"]),
                                    headers=headers)
            # print('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA', file=sys.stderr)
            requested_build = {["job_id": {"pipeline_id": 0, "branch": 0, "commit": 0 "job_name": 0,
                                        "stage": 0, "status": 0, "url": 0}]}
            for item in response.json():
                print(item, file=sys.stderr)
                print('\n', file=sys.stderr)

            # print('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA', file=sys.stderr)
            response.raise_for_status()
        except HTTPError as http_error:
            dict_error = {"status_code":
                          http_error.response.status_code}
            raise HTTPError(json.dumps(dict_error))
        else:
            request_build = response.json()
            return request_build[0]

    def get_project_id(self, project_owner, project_name):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.GITLAB_API_TOKEN
        }
        project_url = project_owner + "%2F" + project_name
        try:
            response = requests.get('https://gitlab.com/api/'
                                    'v4/projects/{project_url}'
                                    .format(project_url=project_url),
                                    headers=headers)
            response.raise_for_status()
        except HTTPError as http_error:
            dict_error = {"status_code":
                          http_error.response.status_code}
            raise HTTPError(json.dumps(dict_error))
        else:
            requested_id = response.json()
            return requested_id
