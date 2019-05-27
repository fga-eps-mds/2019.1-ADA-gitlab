import json
from gitlab.tests.base import BaseTestCase
from gitlab.tests.jsonschemas.report.schemas import\
    ping_schema, report_invalid_project_id_schema
from jsonschema import validate
from gitlab.report.utils import Report
from gitlab.data.user import User
from gitlab.data.project import Project
import os
from requests.exceptions import HTTPError


class TestReport(BaseTestCase):
    def setup(self):
        super().setUp()
        Project.drop_collection()
        User.drop_collection()

    def test_ping_pong(self):
        response = self.client.get("/report/ping")
        data = json.loads(response.data.decode())
        ping_string = json.dumps(ping_schema)
        ping_json = json.loads(ping_string)
        self.assertEqual(response.status_code, 200)
        validate(data, ping_json)

    def test_get_branch(self):
        GITLAB_API_TOKEN = os.getenv("GITLAB_API_TOKEN", "")
        report = Report(GITLAB_API_TOKEN)
        project_id = "11754240"
        report.get_branches(project_id)
        self.assertNotEqual(0, report.repo['branches']
                            ['name'])

    def test_get_branch_invalid_id(self):
        GITLAB_API_TOKEN = os.getenv("GITLAB_API_TOKEN", "")
        report = Report(GITLAB_API_TOKEN)
        project_id = "2490185901"
        with self.assertRaises(HTTPError) as context:
            report.get_branches(project_id)
        invalid_project_id = json.loads(str(context.exception))
        self.assertTrue(invalid_project_id["status_code"], 404)
        validate(invalid_project_id, report_invalid_project_id_schema)

    def test_get_commit(self):
        GITLAB_API_TOKEN = os.getenv("GITLAB_API_TOKEN", "")
        report = Report(GITLAB_API_TOKEN)
        project_id = "11754240"
        report.get_commits(project_id)
        self.assertNotEqual(0, report.repo["commits"]
                                          ["last_commit"]["title"])

    def test_get_commit_invalid_id(self):
        GITLAB_API_TOKEN = os.getenv("GITLAB_API_TOKEN", "")
        report = Report(GITLAB_API_TOKEN)
        project_id = "2490185901"
        with self.assertRaises(HTTPError) as context:
            report.get_commits(project_id)
        invalid_project_id = json.loads(str(context.exception))
        self.assertTrue(invalid_project_id["status_code"], 404)
        validate(invalid_project_id, report_invalid_project_id_schema)

    def test_get_project(self):
        GITLAB_API_TOKEN = os.getenv("GITLAB_API_TOKEN", "")
        report = Report(GITLAB_API_TOKEN)
        project_owner = "adabot"
        project_name = "ada-gitlab"
        report.get_project(project_owner, project_name)
        self.assertNotEqual(0, report.repo["project"]["name"])

    def test_get_pipeline(self):
        GITLAB_API_TOKEN = os.getenv("GITLAB_API_TOKEN", "")
        report = Report(GITLAB_API_TOKEN)
        project_id = "11754240"
        report.get_pipeline(project_id)
        self.assertNotEqual(0, report.repo["pipelines"]
                                          ["number_of_pipelines"])

    def test_get_pipeline_invalid_project_id(self):
        GITLAB_API_TOKEN = os.getenv("GITLAB_API_TOKEN", "")
        report = Report(GITLAB_API_TOKEN)
        project_id = "2380084848"
        with self.assertRaises(HTTPError) as context:
            report.get_pipeline(project_id)
        invalid_project_id = json.loads(str(context.exception))
        self.assertTrue(invalid_project_id["status_code"], 404)
        validate(invalid_project_id, report_invalid_project_id_schema)

    def test_get_pipeline_thirty_days(self):
        GITLAB_API_TOKEN = os.getenv("GITLAB_API_TOKEN", "")
        report = Report(GITLAB_API_TOKEN)
        project_id = "11754240"
        report.get_pipeline(project_id)
        self.assertNotEqual(0, report.repo["pipelines"]
                                          ["number_of_pipelines"])

    def test_repo_information(self):
        GITLAB_API_TOKEN = os.getenv("GITLAB_API_TOKEN", "")
        report = Report(GITLAB_API_TOKEN)
        user = User()
        user.gitlab_user = "adabot"
        project = Project()
        project.project_id = "11754240"
        project.name = "ada-gitlab"
        report.repo_informations(user, project)
        self.assertNotEqual(0, report.repo["project"]
                                          ["name"])
