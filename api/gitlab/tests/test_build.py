import json
import unittest
from gitlab.tests.base import BaseTestCase
from gitlab.tests.jsonschemas.build.schemas import\
    ping_schema, valid_schema, unauthorized_schema,\
    invalid_project_schema, build_valid_schema,\
    build_invalid_schema
from jsonschema import validate
from gitlab.build.build_utils import Build
from gitlab.data.user import User
from gitlab.data.project import Project
import os


class TestBuild(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.user = User()
        self.user.username = 'joaovitor'
        self.user.chat_id = '1234'
        self.user.gitlab_user = 'joaovitor3'
        self.user.gitlab_user_id = '1195203'
        self.user.save()
        self.project = Project()
        self.project_name = 'ada-gitlab'
        self.project_id = '11789629'
        self.project.save_webhook_infos(self.user, self.project_name,
                                        self.project_id)
        self.user.save_gitlab_repo_data(self.project)
        self.GITLAB_API_TOKEN = os.getenv("GITLAB_API_TOKEN", "")
        self.build = Build(self.GITLAB_API_TOKEN)

    def test_ping_pong(self):
        response = self.client.get("/build/ping")
        data = json.loads(response.data.decode())
        ping_string = json.dumps(ping_schema)
        ping_json = json.loads(ping_string)
        self.assertEqual(response.status_code, 200)
        validate(data, ping_json)

    def test_view_get_project_build(self):
        response = self.client.get("/build/{chat_id}"
                                   .format(chat_id=self.user.chat_id))
        data = json.loads(response.data.decode())
        build_string = json.dumps(build_valid_schema)
        build_json = json.loads(build_string)
        self.assertEqual(response.status_code, 200)
        validate(data, build_json)

    def test_view_get_project_build_invalid_project(self):
        chat_id = "8212"
        response = self.client.get("/build/{chat_id}"
                                   .format(chat_id=chat_id))
        invalid_project_json = json.loads(response.data.decode())
        with self.assertRaises(AttributeError) as context:
            self.build.get_project_build(chat_id)
        unauthorized_json = json.loads(str(context.exception))
        self.assertTrue(unauthorized_json["status_code"], 404)
        validate(invalid_project_json, build_invalid_schema)

    def test_get_project_build(self):
        requested_build = self.build.get_project_build(self.project.project_id)
        validate(requested_build, valid_schema)

    def test_get_project_build_invalid_token(self):
        GITLAB_API_TOKEN = "wrong_token"
        build = Build(GITLAB_API_TOKEN)
        with self.assertRaises(AttributeError) as context:
            build.get_project_build(self.project.project_id)
        unauthorized_json = json.loads(str(context.exception))
        self.assertTrue(unauthorized_json["status_code"], 401)
        validate(unauthorized_json, unauthorized_schema)

    def test_get_project_build_invalid_project(self):
        project_id = "182"
        with self.assertRaises(AttributeError) as context:
            self.build.get_project_build(project_id)
        invalid_project_json = json.loads(str(context.exception))
        self.assertTrue(invalid_project_json["status_code"], 404)
        validate(invalid_project_json, invalid_project_schema)


if __name__ == "__main__":
    unittest.main()
