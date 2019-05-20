# api/gitlab/__init__.py

import requests
from requests.exceptions import HTTPError
import json
from gitlab.utils.gitlab_utils import GitlabUtils
from gitlab.data.user import User



class Pipeline(GitlabUtils):
    def __init__(self, GITLAB_API_TOKEN):
        super().__init__(GITLAB_API_TOKEN)

    def get_project_pipeline(self, project_id):
        try:
            response = requests.get(self.GITLAB_API_URL +
                                    "projects/{project_id}/pipelines"
                                    .format(project_id=project_id),
                                    headers=self.headers)
            response.raise_for_status()
            requested_pipeline = response.json()
        except HTTPError as http_error:
            dict_error = {"status_code": http_error.response.status_code}
            raise HTTPError(json.dumps(dict_error))
        except AttributeError:
            dict_error = {"status_code": 404}
            raise AttributeError(json.dumps(dict_error))
        else:            
            if not len(requested_pipeline):
                dict_error = {"status_code": 404}
                raise HTTPError(json.dumps(dict_error))
            return requested_pipeline[0]
