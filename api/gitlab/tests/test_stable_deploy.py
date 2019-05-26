import json
from gitlab.tests.base import BaseTestCase
from jsonschema import validate
from gitlab.stable_deploy.utils import StableDeploy
import os
from gitlab.data.user import User
from gitlab.data import init_db
from gitlab.data.project import Project
from gitlab.tests.jsonschemas.stable_deploy.schemas import\
    ping_schema, stable_deploy_schema, invalid_project_schema
from requests.exceptions import HTTPError


class TestStableDeploy(BaseTestCase):
    GITLAB_API_TOKEN = os.getenv("GITLAB_API_TOKEN", "")

    def setup(self):
        init_db()
        Project.drop_collection()
        User.drop_collection()

    def test_utils_run_stable_deploy(self):
        GITLAB_API_TOKEN = os.getenv("GITLAB_API_TOKEN", "")
        pipeline_id = "63226442"
        project_id = "12532279"
        stable_deploy = StableDeploy(GITLAB_API_TOKEN)
        deploy_status = stable_deploy.run_stable_deploy(project_id,
                                                        pipeline_id)
        validate(deploy_status, stable_deploy_schema)

    def test_utils_run_stable_deploy_wrong_project_id(self):
        GITLAB_API_TOKEN = os.getenv("GITLAB_API_TOKEN", "")
        pipeline_id = "63226442"
        project_id = "abcedfg"
        stable_deploy = StableDeploy(GITLAB_API_TOKEN)
        with self.assertRaises(HTTPError) as context:
            stable_deploy.run_stable_deploy(project_id,
                                            pipeline_id)
        invalid_project_id = json.loads(str(context.exception))
        self.assertTrue(invalid_project_id["status_code"], 404)
        validate(invalid_project_id, invalid_project_schema)

    def test_utils_find_latest_stable_version(self):
        GITLAB_API_TOKEN = os.getenv("GITLAB_API_TOKEN", "")
        project_id = "12532279"
        stable_deploy = StableDeploy(GITLAB_API_TOKEN)
        pipeline_id = stable_deploy.find_latest_stable_version(project_id)
        self.assertIsInstance(pipeline_id, int)

    def test_utils_find_latest_stable_version_wrong_project_id(self):
        GITLAB_API_TOKEN = os.getenv("GITLAB_API_TOKEN", "")
        project_id = "abcdefg"
        stable_deploy = StableDeploy(GITLAB_API_TOKEN)

        with self.assertRaises(HTTPError) as context:
            stable_deploy.find_latest_stable_version(project_id)
        invalid_project_id = json.loads(str(context.exception))
        self.assertTrue(invalid_project_id["status_code"], 404)
        validate(invalid_project_id, invalid_project_schema)

    def test_views_ping_pong(self):
        response = self.client.get("/rerun_pipeline/ping")
        data = json.loads(response.data.decode())
        ping_string = json.dumps(ping_schema)
        ping_json = json.loads(ping_string)
        self.assertEqual(response.status_code, 200)
        validate(data, ping_json)

    def test_views_stable_deploy(self):
        user = User()
        user.chat_id = "00000"
        user.save()
        project = Project()
        project.project_id = "12532279"
        project.user_id = user.id
        project.save()
        user.project = project
        user.save()
        response = self.client.get("/stable_deploy/{chat_id}".format(
                                    chat_id=user.chat_id))
        data = json.loads(response.data.decode())
        User.delete(user)
        Project.delete(project)
        self.assertEqual(response.status_code, 200)
        validate(data, stable_deploy_schema)

    def test_views_stable_deploy_invalid_project_id(self):
        user = User()
        user.chat_id = "00000"
        user.save()
        project = Project()
        project.project_id = "abcdefg"
        project.user_id = user.id
        project.save()
        user.project = project
        user.save()
        response = self.client.get("/stable_deploy/{chat_id}".format(
                            chat_id=user.chat_id))
        User.delete(user)
        Project.delete(project)

        data = json.loads(response.data.decode())
        stable_deploy_string = json.dumps(invalid_project_schema)
        stable_deploy_json = json.loads(stable_deploy_string)

        self.assertEqual(response.status_code, 404)
        validate(data, stable_deploy_json)

    def test_views_stable_deploy_invalid_chat_id(self):
        user = User()
        user.chat_id = "00000"
        user.save()
        project = Project()
        project.project_id = "12532279"
        project.user_id = user.id
        project.save()
        user.project = project
        user.save()
        response = self.client.get("/stable_deploy/{chat_id}".format(
                            chat_id=None))
        User.delete(user)
        Project.delete(project)

        data = json.loads(response.data.decode())
        stable_deploy_string = json.dumps(invalid_project_schema)
        stable_deploy_json = json.loads(stable_deploy_string)

        self.assertEqual(response.status_code, 404)
        validate(data, stable_deploy_json)
