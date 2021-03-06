# api/gitlab/__init__.py

from requests.exceptions import HTTPError
import json
from gitlab.utils.gitlab_utils import GitlabUtils


class Pipeline(GitlabUtils):
    def __init__(self, chat_id):
        super().__init__(chat_id)

    def get_project_pipeline(self, project_id):
        url = self.GITLAB_API_URL +\
                "projects/{project_id}/pipelines"\
                .format(project_id=project_id)
        project_pipeline = self.get_request(url)
        if not len(project_pipeline):
            dict_error = {"status_code": 404}
            raise HTTPError(json.dumps(dict_error))
        return project_pipeline[0]
