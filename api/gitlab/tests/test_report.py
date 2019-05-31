import json
from gitlab.tests.base import BaseTestCase
from gitlab.tests.jsonschemas.report.schemas import\
    valid_branches_schema, valid_commits_schema,\
    valid_pipelines_schema, valid_project_schema
from jsonschema import validate
from gitlab.report.branch_utils import ReportBranches
from gitlab.report.commit_utils import ReportCommits
from gitlab.report.pipeline_report_utils import ReportPipelines
from gitlab.report.report_utils import Report


class TestReport(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.report = Report(self.user.chat_id)
        self.report_branch = ReportBranches(self.user.chat_id)
        self.report_commit = ReportCommits(self.user.chat_id)
        self.report_pipeline = ReportPipelines(self.user.chat_id)

    def test_get_branches(self):
        project_id = "11754240"
        branch_data = self.report_branch.get_branches(project_id)
        self.assertIsInstance(branch_data["branches"], list)

    def test_get_commit(self):
        commit = self.report_commit.get_commits(self.project.project_id)
        self.assertIsInstance(commit["commits"], dict)

    def test_get_pipeline(self):
        pipeline = self.report_pipeline.get_pipeline(self.project.project_id)
        self.assertIsInstance(pipeline["pipeline"], dict)

    def test_get_pipeline_30_days(self):
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

    def test_views_get_branches(self):
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

    def test_views_get_commits(self):
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

    def test_views_get_pipelines(self):
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
