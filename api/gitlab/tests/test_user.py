import json
import unittest
from gitlab.tests.base import BaseTestCase
from gitlab.tests.jsonschemas.user.schemas import\
    ping_schema, valid_schema, unauthorized_schema,\
    invalid_project_schema, user_valid_schema,\
    user_invalid_schema
from jsonschema import validate
from gitlab.user.utils import User
from requests.exceptions import HTTPError
import os


class TestUser(BaseTestCase):
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

    def test_view_get_project_user_invalid_project(self):
        project_owner = "wrong_name"
        response = self.client.get("/user/{project_owner}"
                                   .format(project_owner=project_owner))
        invalid_project_json = json.loads(response.data.decode())
        self.assertTrue(invalid_project_json["status_code"], 404)
        validate(invalid_project_json, user_invalid_schema)

    def test_get_project_user(self):
        GITLAB_API_TOKEN = os.getenv("GITLAB_API_TOKEN", "")
        user = User(GITLAB_API_TOKEN)
        project_owner = "sudjoao"
        requested_user = user.get_project_user(project_owner,
                                            )
        validate(requested_user, valid_schema)

    def test_get_project_user_invalid_token(self):
        GITLAB_API_TOKEN = "wrong_token"
        user = User(GITLAB_API_TOKEN)
        project_owner = "sudjoao"
        with self.assertRaises(HTTPError) as context:
            user.get_project_user(project_owner)
        unauthorized_json = json.loads(str(context.exception))
        self.assertTrue(unauthorized_json["status_code"], 401)
        validate(unauthorized_json, unauthorized_schema)

    def test_get_project_user_invalid_project(self):
        GITLAB_API_TOKEN = os.getenv("GITLAB_API_TOKEN", "")
        user = User(GITLAB_API_TOKEN)
        project_owner = "wrong_name"
        with self.assertRaises(HTTPError) as context:
            user.get_project_user(project_owner)
        invalid_project_json = json.loads(str(context.exception))
        self.assertTrue(invalid_project_json["status_code"], 404)
        validate(invalid_project_json, invalid_project_schema)


if __name__ == "__main__":
    unittest.main()
