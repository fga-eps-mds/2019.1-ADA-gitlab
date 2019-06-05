import json
from gitlab.tests.base import BaseTestCase
from gitlab.tests.jsonschemas.gitlab_utils.schemas import\
     invalid_project_schema
from jsonschema import validate
from gitlab.build.build_utils import Build
from gitlab.utils.gitlab_utils import GitlabUtils
from gitlab.pipeline.pipeline_utils import Pipeline
from gitlab.report.report_utils import Report
from requests.exceptions import HTTPError
from unittest.mock import patch


class TestGitlabUtils(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.build = Build(self.user.chat_id)
        self.pipeline = Pipeline(self.user.chat_id)
        self.report = Report(self.user.chat_id)
        self.gitlab_utils = GitlabUtils(self.user.chat_id)

    @patch('gitlab.utils.gitlab_utils.GitlabUtils.get_request')
    def test_get_project_id(self, mocked_get_request):
        mocked_get_request.return_value = {"id": 12532279,
                                           "description": None,
                                           "name": "Ada-gitlab",
                                           "path": "ada-gitlab",
                                           "default_branch": "master",
                                           "tag_list": [],
                                           "avatar_url": None,
                                           "star_count": 0,
                                           "forks_count": 0}
        project_id = self.gitlab_utils.get_project_id(self.user.gitlab_user,
                                                      self.project.name)
        self.assertIsInstance(project_id, int)

    def test_check_project_exists_not_project_pipeline(self):
        with self.assertRaises(HTTPError) as context:
            self.gitlab_utils.check_project_exists(None, self.pipeline, None)
        unauthorized_json = json.loads(str(context.exception))
        self.assertTrue(unauthorized_json["status_code"], 404)
        validate(unauthorized_json, invalid_project_schema)

    def test_check_project_exists_not_project_build(self):
        with self.assertRaises(HTTPError) as context:
            self.gitlab_utils.check_project_exists(None, self.build, None)
        unauthorized_json = json.loads(str(context.exception))
        self.assertTrue(unauthorized_json["status_code"], 404)
        validate(unauthorized_json, invalid_project_schema)

    def test_check_project_exists_not_project_report(self):
        with self.assertRaises(HTTPError) as context:
            self.gitlab_utils.check_project_exists(None, self.report, None)
        unauthorized_json = json.loads(str(context.exception))
        self.assertTrue(unauthorized_json["status_code"], 404)
        validate(unauthorized_json, invalid_project_schema)
