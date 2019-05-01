import json
import unittest
from gitlab.tests.base import BaseTestCase
from gitlab.tests.jsonschemas.build.schemas import\
    ping_schema, valid_schema, unauthorized_schema,\
    invalid_project_schema, build_valid_schema,\
    build_invalid_schema
from jsonschema import validate
from gitlab.build.utils import Build
from gitlab.data.user import User
from gitlab.data import init_db
from gitlab.data.project import Project
import os


class TestBuild(BaseTestCase):
    def setup(self):
        init_db()
        Project.drop_collection()
        User.drop_collection()

    def test_ping_pong(self):
        response = self.client.get("/build/ping")
        data = json.loads(response.data.decode())
        ping_string = json.dumps(ping_schema)
        ping_json = json.loads(ping_string)
        self.assertEqual(response.status_code, 200)
        validate(data, ping_json)

    def test_view_get_project_build(self):
        user = User()
        user.username = 'joaovitor'
        user.chat_id = '1234'
        user.gitlab_user = 'joaovitor3'
        user.gitlab_user_id = '1195203'
        user.save()
        project = Project()
        project_name = 'ada-gitlab'
        project_id = '11789629'
        project.save_webhook_infos(user, project_name, project_id)
        user.save_gitlab_repo_data(user, project)
        response = self.client.get("/build/{chat_id}"
                                   .format(chat_id=user.chat_id))
        data = json.loads(response.data.decode())
        build_string = json.dumps(build_valid_schema)
        build_json = json.loads(build_string)
        self.assertEqual(response.status_code, 200)
        validate(data, build_json)

    def test_view_get_project_build_invalid_project(self):
        GITLAB_API_TOKEN = os.getenv("GITLAB_API_TOKEN", "")
        build = Build(GITLAB_API_TOKEN)
        chat_id = "8212"
        response = self.client.get("/build/{chat_id}"
                                   .format(chat_id=chat_id))
        invalid_project_json = json.loads(response.data.decode())
        with self.assertRaises(AttributeError) as context:
            build.get_project_build(chat_id)
        unauthorized_json = json.loads(str(context.exception))
        self.assertTrue(unauthorized_json["status_code"], 404)
        validate(invalid_project_json, build_invalid_schema)

    def test_get_project_build(self):
        GITLAB_API_TOKEN = os.getenv("GITLAB_API_TOKEN", "")

        user = User()
        user.username = 'joaovitor'
        user.chat_id = '1234'
        user.gitlab_user = 'joaovitor3'
        user.gitlab_user_id = '1195203'
        user.save()
        project = Project()
        project_name = 'ada-gitlab'
        project_id = '11789629'
        project.save_webhook_infos(user, project_name, project_id)
        user.save_gitlab_repo_data(user, project)
        build = Build(GITLAB_API_TOKEN)
        requested_build = build.get_project_build(project.project_id)
        validate(requested_build, valid_schema)

    def test_get_project_build_invalid_token(self):
        GITLAB_API_TOKEN = "wrong_token"
        build = Build(GITLAB_API_TOKEN)
        user = User()
        user.username = 'joaovitor'
        user.chat_id = '1234'
        user.gitlab_user = 'joaovitor3'
        user.gitlab_user_id = '1195203'
        user.save()
        project = Project()
        project_name = 'ada-gitlab'
        project_id = '11789629'
        project.save_webhook_infos(user, project_name, project_id)
        user.save_gitlab_repo_data(user, project)
        with self.assertRaises(AttributeError) as context:
            build.get_project_build(project.project_id)
        unauthorized_json = json.loads(str(context.exception))
        self.assertTrue(unauthorized_json["status_code"], 401)
        validate(unauthorized_json, unauthorized_schema)

    def test_get_project_build_invalid_project(self):
        GITLAB_API_TOKEN = os.getenv("GITLAB_API_TOKEN", "")
        build = Build(GITLAB_API_TOKEN)
        project_id = "182"
        with self.assertRaises(AttributeError) as context:
            build.get_project_build(project_id)
        invalid_project_json = json.loads(str(context.exception))
        self.assertTrue(invalid_project_json["status_code"], 404)
        validate(invalid_project_json, invalid_project_schema)


if __name__ == "__main__":
    unittest.main()
