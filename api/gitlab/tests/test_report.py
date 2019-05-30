import json
from gitlab.tests.base import BaseTestCase
from gitlab.tests.jsonschemas.report.schemas import\
    unauthorized_schema
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
        self.report_branch.get_branches(project_id)
        self.assertNotEqual(0, self.report_branch.repo['branches']
                            ['name'])

    def test_get_commit(self):
        self.report_commit.get_commits(self.project.project_id)
        self.assertNotEqual(0, self.report_commit.repo["commits"]
                                                      ["last_commit"]["title"])

    def test_get_pipeline(self):
        self.report_pipeline.get_pipeline(self.project.project_id)
        repo = self.report_pipeline.repo
        self.assertNotEqual(0, (repo["pipelines"]["number_of_pipelines"]))

    def test_get_project(self):
        self.report.get_project(self.user.gitlab_user,
                                self.project.name)
        self.assertNotEqual(0, self.report.repo["project"]
                                               ["name"])

    def test_repo_information(self):
        self.report.repo_informations(self.user, self.project)
        self.assertNotEqual(0, self.report.repo["project"]
                                               ["name"])

    # def test_view_generate_report(self):
    #     response = self.client.get("/report/{chat_id}"
    #                                .format(chat_id=self.user.chat_id))
    #     data = json.loads(response.data.decode())
    #     self.assertEqual(response.status_code, 200)
    #     validate(data, report_valid_schema)
    def test_view_generate_report_wrong_chat_id(self):
        chat_id = "632186121234"
        response = self.client.get("/report/{chat_id}"
                                   .format(chat_id=chat_id))
        invalid_project_json = json.loads(response.data.decode())
        self.assertTrue(invalid_project_json["status_code"], 404)
        validate(invalid_project_json, unauthorized_schema)
