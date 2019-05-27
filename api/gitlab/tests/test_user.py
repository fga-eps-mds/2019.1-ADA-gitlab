import json
import unittest
from gitlab.tests.base import BaseTestCase
from gitlab.data.user import User
from gitlab.tests.jsonschemas.user.schemas import\
    ping_schema, valid_schema, unauthorized_schema, \
    user_valid_schema, test_view_get_user_id_schema,\
    user_invalid_schema, utils_get_user_schema,\
    test_view_get_project_id_schema
from jsonschema import validate
from gitlab.user.utils import UserUtils
from requests.exceptions import HTTPError
import os

GITLAB_API_TOKEN = os.environ.get("GITLAB_API_TOKEN", "")


class TestUser(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.user = User()
        self.user.access_token = str(GITLAB_API_TOKEN)
        self.user.username = "sudjoao"
        self.user.chat_id = "662358971"
        self.user.save()

    def test_ping_pong(self):
        response = self.client.get("/user/ping")
        data = json.loads(response.data.decode())
        ping_string = json.dumps(ping_schema)
        ping_json = json.loads(ping_string)
        self.assertEqual(response.status_code, 200)
        validate(data, ping_json)

    def test_view_get_project_user(self):
        project_owner = "sudjoao"
        response = self.client.get("/user/{project_owner}"
                                   .format(project_owner=project_owner))
        data = json.loads(response.data.decode())
        user_string = json.dumps(user_valid_schema)
        user_json = json.loads(user_string)
        self.assertEqual(response.status_code, 200)
        validate(data, user_json)

    def test_invalid_view_get_project_user(self):
        response = self.client.get("/user/{project_owner}"
                                   .format(project_owner="invalid"))
        data = json.loads(response.data.decode())
        user_string = json.dumps(user_invalid_schema)
        user_json = json.loads(user_string)
        self.assertEqual(response.status_code, 404)
        validate(data, user_json)

    def test_view_get_project_user_invalid_project(self):
        project_owner = "wrong_name"
        response = self.client.get("/user/{project_owner}"
                                   .format(project_owner=project_owner))
        invalid_project_json = json.loads(response.data.decode())
        self.assertTrue(invalid_project_json["status_code"], 404)
        validate(invalid_project_json, user_invalid_schema)

    def test_get_project_user(self):
        GITLAB_API_TOKEN = os.getenv("GITLAB_API_TOKEN", "")
        user = UserUtils(GITLAB_API_TOKEN)
        project_owner = "sudjoao"
        requested_user = user.get_project_user(project_owner)
        validate(requested_user, valid_schema)

    def test_get_project_user_invalid_token(self):
        GITLAB_API_TOKEN = "wrong_token"
        user = UserUtils(GITLAB_API_TOKEN)
        project_owner = "sudjoao"
        with self.assertRaises(HTTPError) as context:
            user.get_project_user(project_owner)
        unauthorized_json = json.loads(str(context.exception))
        self.assertTrue(unauthorized_json["status_code"], 401)
        validate(unauthorized_json, unauthorized_schema)

    def test_get_project_user_invalid_project(self):
        GITLAB_API_TOKEN = os.getenv("GITLAB_API_TOKEN", "")
        user = UserUtils(GITLAB_API_TOKEN)
        project_owner = "wrong_project"
        with self.assertRaises(IndexError) as context:
            user.get_project_user(project_owner)
        self.assertTrue(str(context.exception), "list index out of range")

    def test_utils_send_message(self):
        userinfo = UserUtils(GITLAB_API_TOKEN)
        userinfo.send_message(GITLAB_API_TOKEN, self.user.chat_id)

    def test_select_repos_by_button(self):
        userinfo = UserUtils(GITLAB_API_TOKEN)
        header = {"Content-Type": "application/json"}
        userinfo.select_repos_by_buttons(self.user.username, header)

    def test_utils_get_user(self):
        userinfo = UserUtils(GITLAB_API_TOKEN)
        dat = userinfo.get_user()
        data = dat
        ping_string = json.dumps(utils_get_user_schema)
        ping_json = json.loads(ping_string)
        validate(data, ping_json)

    def test_view_get_user_id(self):
        response = self.client.get("/user/id/{project_owner}".format(
                                   project_owner=self.user.username))
        data = json.loads(response.data.decode())
        ping_string = json.dumps(test_view_get_user_id_schema)
        ping_json = json.loads(ping_string)
        self.assertEqual(response.status_code, 200)
        validate(data, ping_json)

    def test_invalid_view_get_user_id(self):
        response = self.client.get("/user/id/{project_owner}".format(
                                   project_owner="123213"))
        data = json.loads(response.data.decode())
        ping_string = json.dumps(user_invalid_schema)
        ping_json = json.loads(ping_string)
        self.assertEqual(response.status_code, 404)
        validate(data, ping_json)

    def test_view_get_project_id(self):
        response = self.client.get("/user/repo/{project_owner}/{project_name}"
                                   .format(project_owner=self.user.username,
                                           project_name="ada-gitlab"))
        data = json.loads(response.data.decode())
        ping_string = json.dumps(test_view_get_project_id_schema)
        ping_json = json.loads(ping_string)
        self.assertEqual(response.status_code, 200)
        validate(data, ping_json)

    def test_invalid_view_get_project_id(self):
        response = self.client.get("/user/repo/{project_owner}/{project_name}"
                                   .format(project_owner="invalid",
                                           project_name="invalid"))
        data = json.loads(response.data.decode())
        ping_string = json.dumps(user_invalid_schema)
        ping_json = json.loads(ping_string)
        self.assertEqual(response.status_code, 404)
        validate(data, ping_json)

    def test_view_get_access_token(self):
        response = self.client.get("/user/gitlab/authorize")
        self.assertEquals(response.status_code, 302)


if __name__ == "__main__":
    unittest.main()
