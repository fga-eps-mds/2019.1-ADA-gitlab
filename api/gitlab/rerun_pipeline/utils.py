import requests
from requests.exceptions import HTTPError
import json


class RerunPipeline():

    def __init__(self, GITLAB_API_TOKEN):
        self.GITLAB_API_TOKEN = GITLAB_API_TOKEN

    def rerun_pipeline(self, project_id, pipeline_id):
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.GITLAB_API_TOKEN
        }
        url = ("https://gitlab.com/api/v4/projects/"
               "{project_id}/pipelines/{pipeline_id}"
               "/retry".format(project_id=project_id,
                               pipeline_id=pipeline_id))
        try:
            response = requests.post(url="{url}".format(url=url),
                                     headers=headers)
        except HTTPError as http_error:
            dict_error = {"status_code": http_error.response.status_code}
            raise HTTPError(json.dumps(dict_error))
        else:
            restart_status = response.json()
            return restart_status

    def get_pipelines(self, project_id):
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.GITLAB_API_TOKEN
        }
        try:
            response = requests.get("https://gitlab.com/api/"
                                    "v4/projects/{project_id}/pipelines"
                                    .format(project_id=project_id),
                                    headers=headers)
            response.raise_for_status()
        except HTTPError as http_error:
            dict_error = {"status_code": http_error.response.status_code}
            raise HTTPError(json.dumps(dict_error))
        except AttributeError:
            dict_error = {"status_code": 404}
            raise AttributeError(json.dumps(dict_error))
        else:
            requested_pipeline = response.json()
            if len(requested_pipeline) == 0:
                dict_error = {"status_code": 404}
                raise HTTPError(json.dumps(dict_error))
            return requested_pipeline