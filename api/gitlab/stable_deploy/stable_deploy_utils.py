from requests import post
from requests.exceptions import HTTPError
import json
from gitlab.utils.gitlab_utils import GitlabUtils


class StableDeploy(GitlabUtils):
    def __init__(self, chat_id):
        super().__init__(chat_id)

    def run_stable_deploy(self, project_id, pipeline_id):
        url = ("https://gitlab.com/api/v4/projects/"
               "{project_id}/pipelines/{pipeline_id}"
               "/retry".format(project_id=project_id,
                               pipeline_id=pipeline_id))
        try:
            response = post(url=url,
                            headers=self.headers)
            response.raise_for_status()
        except HTTPError as http_error:
            dict_error = {"status_code": http_error.response.status_code}
            raise HTTPError(json.dumps(dict_error))
        else:
            deploy_status = {"status": "success"}
            return deploy_status

    def find_latest_stable_version(self, project_id):
        url = ("https://gitlab.com/api/v4/projects/"
               "{project_id}/pipelines/".format(project_id=project_id))
        pipelines = self.get_request(url)
        for item in pipelines:
            if item["status"] == "success":
                pipeline_id = item["id"]
                break
        return pipeline_id
