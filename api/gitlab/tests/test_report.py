import json
from gitlab.tests.base import BaseTestCase
from gitlab.tests.jsonschemas.report.schemas import\
    valid_branches_schema, valid_commits_schema,\
    valid_pipelines_schema, valid_project_schema,\
    pipeline_invalid_schema
from jsonschema import validate
from gitlab.report.branch_utils import ReportBranches
from gitlab.report.commit_utils import ReportCommits
from gitlab.report.pipeline_report_utils import ReportPipelines
from gitlab.report.report_utils import Report
from unittest.mock import patch
from requests import Response
from datetime import date, timedelta
from requests.exceptions import HTTPError


class TestReport(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.report = Report(self.user.chat_id)
        self.report_branch = ReportBranches(self.user.chat_id)
        self.report_commit = ReportCommits(self.user.chat_id)
        self.report_pipeline = ReportPipelines(self.user.chat_id)

        self.mocked_get_branches_response = Response()
        self.mocked_get_branches_response.status_code = 200
        mocked_get_branches_content = [{"name": "117-Webhook",
                                        "merged": True,
                                        "protected": False,
                                        "default": False
                                        }]
        get_branches_content_in_binary = json.\
            dumps(mocked_get_branches_content).encode('utf-8')
        self.mocked_get_branches_response._content = \
            get_branches_content_in_binary

        self.mocked_get_pipeline_response = Response()
        self.mocked_get_pipeline_response.status_code = 200
        mocked_get_pipeline_content = [{"id": 63218612,
                                        "sha": "ab063122e7dfbf517",
                                        "ref": "251-Mock",
                                        "status": "failed",
                                        "web_url": "https://gitlab.com/"},
                                       {"id": 63218613,
                                        "sha": "ab063122e7dfbf513",
                                        "ref": "251-Mock",
                                        "status": "success",
                                        "web_url": "https://gitlab.com/"}]
        get_pipeline_content_in_binary = json.\
            dumps(mocked_get_pipeline_content).encode('utf-8')
        self.mocked_get_pipeline_response._content = \
            get_pipeline_content_in_binary

        self.mocked_check_pipeline_date_response = Response()
        self.mocked_check_pipeline_date_response.status_code = 200
        self.mocked_check_pipeline_date_content = {"id": 64938326,
                                                   "ref": "251-Mock",
                                                   "status": "success",
                                                   "created_at":
                                                   str(date.today())}

        check_pipeline_date_content_in_binary = json.\
            dumps(self.mocked_check_pipeline_date_content).encode('utf-8')
        self.mocked_check_pipeline_date_response._content = \
            check_pipeline_date_content_in_binary

        self.mocked_check_pipeline_date_response_2 = Response()
        self.mocked_check_pipeline_date_response_2.status_code = 200
        self.mocked_check_pipeline_date_content_2 = {"id": 64938326,
                                                     "ref": "251-Mock",
                                                     "status": "failed",
                                                     "created_at":
                                                     str(date.today())}

        check_pipeline_date_content_in_binary_2 = json.\
            dumps(self.mocked_check_pipeline_date_content_2).encode('utf-8')
        self.mocked_check_pipeline_date_response_2._content = \
            check_pipeline_date_content_in_binary_2

        self.mocked_get_commits_response = Response()
        self.mocked_get_commits_response.status_code = 200
        mocked_get_commits_content = [{"id": "717b7ea7b105d212c",
                                       "title": "Merge pull request #18",
                                       "author_name": "author",
                                       "author_email": "a@email.com",
                                       "authored_date":
                                       "2019-05-03T07:29:14.000Z",
                                       }]
        get_commits_content_in_binary = json.\
            dumps(mocked_get_commits_content).encode('utf-8')
        self.mocked_get_commits_response._content = \
            get_commits_content_in_binary

    @patch('gitlab.utils.gitlab_utils.get')
    def test_get_branches(self, mocked_get):
        mocked_get.return_value = self.mocked_get_branches_response
        project_id = "11754240"
        branch_data = self.report_branch.get_branches(project_id)
        self.assertIsInstance(branch_data["branches"], list)

    @patch('gitlab.utils.gitlab_utils.GitlabUtils.return_project')
    @patch('gitlab.utils.gitlab_utils.json')
    def test_report_error_message(self, mocked_json, mocked_return_project):
        mocked_return_project.side_effect = HTTPError
        mocked_json.loads.return_value = {"status_code": 404}
        response = self.client.get("/report/project/{chat_id}"
                                   .format(chat_id=self.user.chat_id))
        invalid_project_json = json.loads(response.data.decode())
        self.assertTrue(invalid_project_json["status_code"], 404)
        validate(invalid_project_json, pipeline_invalid_schema)

    @patch('gitlab.utils.gitlab_utils.get')
    def test_get_commit(self, mocked_get):
        mocked_get.return_value = self.mocked_get_commits_response
        commit = self.report_commit.get_commits(self.project.project_id)
        self.assertIsInstance(commit["commits"], dict)

    @patch('gitlab.utils.gitlab_utils.get')
    def test_get_pipeline(self, mocked_get):
        mocked_get.side_effect = (self.mocked_get_pipeline_response,
                                  self.mocked_check_pipeline_date_response,
                                  self.mocked_check_pipeline_date_response_2)

        pipeline = self.report_pipeline.get_pipeline(self.project.project_id)
        self.assertIsInstance(pipeline["pipeline"], dict)

    @patch('gitlab.utils.gitlab_utils.get')
    def test_get_pipeline_30_days(self, mocked_get):
        check_pipeline_date_content = self.mocked_check_pipeline_date_content
        check_pipeline_date_content["created_at"] = str(date.today()
                                                        - timedelta(days=20))
        check_pipeline_date_content_in_binary = json.\
            dumps(check_pipeline_date_content).encode('utf-8')
        self.mocked_check_pipeline_date_response._content = \
            check_pipeline_date_content_in_binary
        mocked_get.side_effect = (self.mocked_get_pipeline_response,
                                  self.mocked_check_pipeline_date_response,
                                  self.mocked_check_pipeline_date_response_2)

        self.user.gitlab_user = "joaovitor3"
        self.project.name = "ada-gitlab"
        self.project.project_id = "11789629"
        self.user.save()
        self.project.save()
        self.report_pipeline.get_pipeline(self.project.project_id)
        repo = self.report_pipeline.repo
        self.project_name = 'ada-gitlab'
        self.project_id = '12532279'
        self.project.save()
        self.user.gitlab_user = "adatestbot"
        self.user.save()
        self.assertNotEqual(0, (repo["pipelines"]["number_of_pipelines"]))

    def test_get_project(self):
        project = self.report.get_project(self.user.gitlab_user,
                                          self.project.name)
        self.assertIsInstance(project["project"], dict)

    @patch('gitlab.utils.gitlab_utils.get')
    def test_views_get_branches(self, mocked_get):
        mocked_get.return_value = self.mocked_get_branches_response
        response = self.client.get("/report/branches/{chat_id}"
                                   .format(chat_id=self.user.chat_id))
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        validate(data, valid_branches_schema)

    def test_views_get_branches_wrong_chat_id(self):
        response = self.client.get("/report/branches/{chat_id}"
                                   .format(chat_id=0000))
        invalid_project_json = json.loads(response.data.decode())
        self.assertTrue(invalid_project_json["status_code"], 404)

    @patch('gitlab.utils.gitlab_utils.get')
    def test_views_get_commits(self, mocked_get):
        mocked_get.return_value = self.mocked_get_commits_response
        response = self.client.get("/report/commits/{chat_id}"
                                   .format(chat_id=self.user.chat_id))
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        validate(data, valid_commits_schema)

    def test_views_get_commits_wrong_chat_id(self):
        response = self.client.get("/report/commits/{chat_id}"
                                   .format(chat_id=0000))
        invalid_project_json = json.loads(response.data.decode())
        self.assertTrue(invalid_project_json["status_code"], 404)

    @patch('gitlab.utils.gitlab_utils.get')
    def test_views_get_pipelines(self, mocked_get):
        check_pipeline_date_content = self.mocked_check_pipeline_date_content
        check_pipeline_date_content["created_at"] = str(date.today()
                                                        - timedelta(days=100))
        check_pipeline_date_content_in_binary = json.\
            dumps(check_pipeline_date_content).encode('utf-8')
        self.mocked_check_pipeline_date_response._content = \
            check_pipeline_date_content_in_binary

        check_pipeline_date_content_2 = self.\
            mocked_check_pipeline_date_content_2
        check_pipeline_date_content_2["created_at"] = str(date.today() -
                                                          timedelta(days=100))
        check_pipeline_date_content_in_binary_2 = json.\
            dumps(check_pipeline_date_content_2).encode('utf-8')
        self.mocked_check_pipeline_date_response_2._content = \
            check_pipeline_date_content_in_binary_2

        mocked_get.side_effect = (self.mocked_get_pipeline_response,
                                  self.mocked_check_pipeline_date_response,
                                  self.mocked_check_pipeline_date_response_2)
        response = self.client.get("/report/pipelines/{chat_id}"
                                   .format(chat_id=self.user.chat_id))
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        validate(data, valid_pipelines_schema)

    def test_views_get_pipelines_wrong_chat_id(self):
        response = self.client.get("/report/pipelines/{chat_id}"
                                   .format(chat_id=0000))
        invalid_project_json = json.loads(response.data.decode())
        self.assertTrue(invalid_project_json["status_code"], 404)

    def test_views_get_project(self):
        response = self.client.get("/report/project/{chat_id}"
                                   .format(chat_id=self.user.chat_id))
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        validate(data, valid_project_schema)

    def test_views_get_project_wrong_chat_id(self):
        response = self.client.get("/report/project/{chat_id}"
                                   .format(chat_id=0000))
        invalid_project_json = json.loads(response.data.decode())
        self.assertTrue(invalid_project_json["status_code"], 404)
