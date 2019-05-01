# api/gitlab/__init__.py

import requests
from requests.exceptions import HTTPError
import json
from gitlab.pipeline.utils import Pipeline


class Build():
    def __init__(self, GITLAB_API_TOKEN):
        self.GITLAB_API_TOKEN = GITLAB_API_TOKEN

    def get_project_build(self, project_id):
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.GITLAB_API_TOKEN
        }
        try:
            pipeline = Pipeline(self.GITLAB_API_TOKEN)
            pipeline_id = pipeline.get_project_pipeline_by_id(
                project_id)
            response = requests.get("https://gitlab.com/api/"
                                    "v4/projects/{project_id}/pipelines/"
                                    "{pipeline_id}/jobs"
                                    .format(project_id=project_id,
                                            pipeline_id=pipeline_id["id"]),
                                    headers=headers)
            build_dict = response.json()
            requested_build = []
            for i, item in enumerate(build_dict):
                job_data = {"job_id": 0, "branch": 0,
                            "commit": 0, "stage": 0,
                            "job_name": 0, "status": 0,
                            "web_url": 0}
                job_data["job_id"] = build_dict[i]["id"]
                job_data["branch"] = build_dict[i]["ref"]
                job_data["commit"] = build_dict[i]["commit"]["title"]
                job_data["stage"] = build_dict[i]["stage"]
                job_data["job_name"] = build_dict[i]["name"]
                job_data["status"] = build_dict[i]["status"]
                job_data["web_url"] = build_dict[i]["web_url"]
                job_data["pipeline_url"] = build_dict[i]["pipeline"]["web_url"]
                requested_build.append(job_data)
            response.raise_for_status()
        except HTTPError as http_error:
            dict_error = {"status_code":
                          http_error.response.status_code}
            raise HTTPError(json.dumps(dict_error))
        else:
            return requested_build

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
            dict_error = {"status_code":
                          http_error.response.status_code}
            raise HTTPError(json.dumps(dict_error))
        else:
            requested_id = response.json()
            return requested_id
