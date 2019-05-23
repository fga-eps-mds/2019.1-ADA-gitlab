# api/gitlab/__init__.py

import requests
from requests.exceptions import HTTPError
import json
from gitlab.pipeline.pipeline_utils import\
     Pipeline 
from gitlab.utils.gitlab_utils import GitlabUtils

import sys
from gitlab.data.user import User
from gitlab.build.error_messages import NOT_FOUND, UNAUTHORIZED
from flask import jsonify



class Build(GitlabUtils):
    def __init__(self, chat_id):
        super().__init__(chat_id)
        
    def get_project_build(self, project_id):
        pipeline = Pipeline(self.chat_id)
        pipeline_id = pipeline.get_project_pipeline(
                                            project_id)
        url = self.GITLAB_API_URL +\
              "projects/{project_id}/pipelines/"\
              "{pipeline_id}/jobs"\
              .format(project_id=project_id,
                    pipeline_id=pipeline_id["id"])
        resp_json = self.get_request(url)
        project_build = self.build_requested_build(resp_json)
        return project_build
    
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

    def build_requested_build(self, resp):
        requested_build = []
        for i, item in enumerate(resp):
            job_data = {"job_id": 0, "branch": 0,
                        "commit": 0, "stage": 0,
                        "job_name": 0, "status": 0,
                        "web_url": 0}
            self.update_job_data(job_data, resp, i)
            requested_build.append(job_data)
        return requested_build
