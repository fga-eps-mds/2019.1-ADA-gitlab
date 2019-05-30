import json
import unittest
from gitlab.tests.base import BaseTestCase
from gitlab.tests.jsonschemas.user.schemas import\
    valid_schema, unauthorized_schema,\
    user_data_valid_schema
from jsonschema import validate
from gitlab.user.utils import UserUtils
from requests.exceptions import HTTPError


class TestUser(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.user_utils = UserUtils(self.user.chat_id)

    def test_get_user_project(self):
        requested_user = self.user_utils.get_user_project(
                                self.user.gitlab_user)
        validate(requested_user, valid_schema)

    def test_get_user_project_invalid_user(self):
        invalid_user = "wrong_user"
        with self.assertRaises(HTTPError) as context:
            self.user_utils.get_user_project(invalid_user)
        unauthorized_json = json.loads(str(context.exception))
        self.assertTrue(unauthorized_json["status_code"], 404)
        validate(unauthorized_json, unauthorized_schema)

    def test_get_user_id(self):
        user_id = self.user_utils.get_user_id(self.user.gitlab_user)
        self.assertIsInstance(user_id, int)

    def test_get_own_user_data(self):
        user_data = self.user_utils.get_own_user_data()
        validate(user_data, user_data_valid_schema)

    def test_select_repos_by_buttons(self):
        buttons = self.user_utils.select_repos_by_buttons(
                                    self.user.gitlab_user)
        self.assertIsInstance(buttons, list)

    def test_send_button_message(self):
        user_data = self.user_utils.get_own_user_data()
        self.user_utils.send_button_message(user_data, self.user.chat_id)


if __name__ == "__main__":
    unittest.main()
    # def test_send_button_message(self):
    #     send_message = self.user_utils.send_button_message(self.user,
    #                                                        self.user.chat_id)
    #     print(send_message, file=sys.stderr)
    # def test_view_get_project_user(self):
    #     project_owner = "sudjoao"
    #     response = self.client.get("/user/{project_owner}"
    #                                .format(project_owner=project_owner))
    #     data = json.loads(response.data.decode())
    #     user_string = json.dumps(user_valid_schema)
    #     user_json = json.loads(user_string)
    #     self.assertEqual(response.status_code, 200)
    #     validate(data, user_json)

    # def test_view_get_project_user_invalid_project(self):
    #     project_owner = "wrong_name"
    #     response = self.client.get("/user/{project_owner}"
    #                                .format(project_owner=project_owner))
    #     invalid_project_json = json.loads(response.data.decode())
    #     self.assertTrue(invalid_project_json["status_code"], 404)
    #     validate(invalid_project_json, user_invalid_schema)
