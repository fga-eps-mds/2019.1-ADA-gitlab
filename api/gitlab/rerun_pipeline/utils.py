import requests
from requests.exceptions import HTTPError
import json


class RerunPipeline():

    project_id = 0

    def __init__(self, GITLAB_API_TOKEN, project):
        self.GITLAB_API_TOKEN = GITLAB_API_TOKEN
        self.project_id = int(project.project_id)

    def rerun_pipeline(self, user, project, pipeline_id):
    '''Sabendo o pipeline_id, reiniciar a pipeline referente a ele'''
        pass

    def get_pipelines(self):
    '''Retornar para a Ada as pipelines e os ids delas do projeto do usuario'''

        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.GITLAB_API_TOKEN
        }
        try:
            response = requests.get("https://gitlab.com/api/v4/projects/"
                                    "{project_id}/pipelines/"
                                    .format(project_id=self.project_id,),
                                    headers=headers)
            pipelines = response.json()
            response.raise_for_status()
        except HTTPError as http_error:
            dict_error = {"status_code": http_error.response.status_code}
            raise HTTPError(json.dumps(dict_error))
        else:
            pipelines_names_ids = {"names": [], "ids": []}
            for i, item in enumerate(pipelines):
                pipelines_names_ids["names"].append(i["ref"])
                pipelines_names_ids["ids"].append(i["id"])

        return pipelines_names_ids
