import json
from gitlab.tests.base import BaseTestCase
from gitlab.tests.jsonschemas.rerun_pipeline.schemas import\
    ping_schema

from jsonschema import validate
from gitlab.rerun_pipeline.utils import RerunPipeline
import os
from gitlab.data.user import User
from gitlab.data.project import Project


class TestRerunPipeline(BaseTestCase):
    GITLAB_API_TOKEN = os.getenv("GITLAB_API_TOKEN", "")

    def setup(self):
        super().setUp()
        Project.drop_collection()
        User.drop_collection()

    def test_rerun_pipeline_ping_pong(self):
        response = self.client.get("/rerun_pipeline/ping")
        data = json.loads(response.data.decode())
        ping_string = json.dumps(ping_schema)
        ping_json = json.loads(ping_string)
        self.assertEqual(response.status_code, 200)
        validate(data, ping_json)

<<<<<<< HEAD
    # def test_views_rerun_pipeline(self):
    #     pipeline_id = "61073494"
    #     chat_id = "123456789"
    #     user = User()
    #     user.create_user("sudjoao")
    #     user.chat_id = chat_id
    #     project = Project()
    #     project.create_project(user, "abc", "ada_gitlab",
    #                            "https://gitlab.com/sudjoao/ada-gitlab/", [],
    #                            "12309295")
    #     user.project = project
    #     user.save()
    #     # Testar
    #     response = self.client.get("/rerun_pipeline/{chat_id}/"
    #                                "{pipeline_id}".format(
    #                                 chat_id=chat_id,
    #                                 pipeline_id=pipeline_id))
    #     User.delete(user)
    #     self.assertEqual(response.status_code, 200)

    # def test_views_rerun_pipeline_wrong_pipeline_id(self):
    #     pipeline_id = "123456"
    #     chat_id = "123456789"
    #     user = User()
    #     user.create_user("sudjoao")
    #     user.chat_id = chat_id
    #     project = Project()
    #     project.create_project(user, "abc", "ada_gitlab",
    #                            "https://gitlab.com/sudjoao/ada-gitlab/", [],
    #                            "12309295")
    #     user.project = project
    #     user.save()
    #     response = self.client.get("/rerun_pipeline/{chat_id}/"
    #                                "{pipeline_id}".format(
    #                                 chat_id=chat_id,
    #                                 pipeline_id=pipeline_id))
    #     User.delete(user)
    #     self.assertEqual(response.status_code, 404)

    # def test_utils_rerun_pipeline(self):
    #     pipeline_id = "61073494"
    #     project_id = "12309295"
    #     rerunpipeline = RerunPipeline(self.GITLAB_API_TOKEN)
    #     response = rerunpipeline.rerun_pipeline(project_id,
    #                                             pipeline_id)
    #     validate(response, rerun_pipeline_schema)
=======
    def test_views_rerun_pipeline(self):
        pipeline_id = "63218612"
        chat_id = "123456789"
        user = User()
        user.create_user("adatestbot")
        user.chat_id = chat_id
        project = Project()
        project.create_project(user, "abc", "ada_gitlab",
                               "https://gitlab.com/adatestbot/ada-gitlab/", [],
                               "12532279")
        user.project = project
        user.save()
        # Testar
        response = self.client.get("/rerun_pipeline/{chat_id}/"
                                   "{pipeline_id}".format(
                                    chat_id=chat_id,
                                    pipeline_id=pipeline_id))
        User.delete(user)
        self.assertEqual(response.status_code, 200)

    def test_views_rerun_pipeline_wrong_pipeline_id(self):
        pipeline_id = "123456"
        chat_id = "123456789"
        user = User()
        user.create_user("sudjoao")
        user.chat_id = chat_id
        project = Project()
        project.create_project(user, "abc", "ada_gitlab",
                               "https://gitlab.com/adatestbot/ada-gitlab/", [],
                               "12532279")
        user.project = project
        user.save()
        response = self.client.get("/rerun_pipeline/{chat_id}/"
                                   "{pipeline_id}".format(
                                    chat_id=chat_id,
                                    pipeline_id=pipeline_id))
        User.delete(user)
        self.assertEqual(response.status_code, 404)

    def test_utils_rerun_pipeline(self):
        pipeline_id = "63218612"
        project_id = "12532279"
        rerunpipeline = RerunPipeline(self.GITLAB_API_TOKEN)
        response = rerunpipeline.rerun_pipeline(project_id,
                                                pipeline_id)
        validate(response, rerun_pipeline_schema)
>>>>>>> devel

    def test_utils_build_buttons(self):
        pipeline_id = "12345678"
        rerun_pipeline = RerunPipeline(self.GITLAB_API_TOKEN)
        buttons = rerun_pipeline.build_buttons(pipeline_id)
        self.assertIsInstance(buttons, list)
