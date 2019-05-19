# api/gitlab/__init__.py

import requests
from requests.exceptions import HTTPError
import json
from gitlab.pipeline.utils import Pipeline
from gitlab.utils.utils import GitlabUtils
import sys

class Build(GitlabUtils):
    def __init__(self, GITLAB_API_TOKEN):
        super().__init__(GITLAB_API_TOKEN) 
        
    def get_project_build(self, project_id):
        try:
            pipeline = Pipeline(self.GITLAB_API_TOKEN)
            try:
                pipeline_id = pipeline.get_project_pipeline(
                    project_id)
            except HTTPError as http_error:
                dict_error = {"status_code":
                              http_error.response.status_code}
                raise HTTPError(json.dumps(dict_error))
            except AttributeError:
                dict_error = {"status_code": 404}
                raise AttributeError(json.dumps(dict_error))
            else:
                response = requests.get("https://gitlab.com/api/"
                                        "v4/projects/{project_id}/pipelines/"
                                        "{pipeline_id}/jobs"
                                        .format(project_id=project_id,
                                                pipeline_id=pipeline_id["id"]),
                                        headers=self.headers)
                response.raise_for_status()
                resp = response.json()
                requested_build = self.build_reqested_build(resp)
        except HTTPError as http_error:
            dict_error = {"status_code":
                          http_error.response.status_code}
            raise HTTPError(json.dumps(dict_error))
        except AttributeError:
            dict_error = {"status_code": 404}
            raise AttributeError(json.dumps(dict_error))
        else:
            return requested_build

    def get_requested_build(self, project):
        if project:
            requested_build = self.get_project_build(project.project_id)
        else:
            dict_error = {"status_code": 404}
            raise HTTPError(json.dumps(dict_error))
        return requested_build
    
    def update_job_data(self, job_dict, resp, count):
        job_dict["pipeline_status"] = resp[count]["status"]
        job_dict["job_id"] = resp[count]["id"]
        job_dict["branch"] = resp[count]["ref"]
        job_dict["commit"] = resp[count]["commit"]["title"]
        job_dict["stage"] = resp[count]["stage"]
        job_dict["job_name"] = resp[count]["name"]
        job_dict["status"] = resp[count]["status"]
        job_dict["web_url"] = resp[count]["web_url"]
        job_dict["pipeline_url"] = resp[count]["pipeline"]["web_url"]

    def build_reqested_build(self, resp):
        requested_build = []
        for i, item in enumerate(resp):
            job_data = {"job_id": 0, "branch": 0,
                        "commit": 0, "stage": 0,
                        "job_name": 0, "status": 0,
                        "web_url": 0}
            self.update_job_data(job_data, resp, i)
            requested_build.append(job_data)
        return requested_build
