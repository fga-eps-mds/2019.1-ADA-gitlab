import requests
from requests.exceptions import HTTPError
import json
import sys
import telegram


class StableDeploy():
    # dar um retry nessa pipeline
    # retornar para ada

    def __init__(self, GITLAB_API_TOKEN):
        self.GITLAB_API_TOKEN = GITLAB_API_TOKEN

    def run_stable_deploy(self, project_id, pipeline_id):
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
            response.raise_for_status()
        except HTTPError as http_error:
            dict_error = {"status_code": http_error.response.status_code}
            raise HTTPError(json.dumps(dict_error))
        else:
            deploy_status = response.json()
            return deploy_status

    def find_latest_stable_version(self, project_id):
        # descobrir qual a ultima pipeline que deu certo e pegar o id dela
        # se nao houver, retornar erro
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.GITLAB_API_TOKEN
        }
        url = ("https://gitlab.com/api/v4/projects/"
               "{project_id}/pipelines/".format(project_id=project_id))
        try:
            response = requests.post(url="{url}".format(url=url),
                                     headers=headers)
            response.raise_for_status()
        except HTTPError as http_error:
            dict_error = {"status_code": http_error.response.status_code}
            raise HTTPError(json.dumps(dict_error))
        else:
            pipelines = response.json()
            pipeline_id = 0
            for i, item in enumerate(pipelines):
                if i["status"] == "success":
                    pipeline_id = i["id"]
                    break
            return pipeline_id
