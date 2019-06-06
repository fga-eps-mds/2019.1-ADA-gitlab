import json
import unittest
from gitlab.tests.base import BaseTestCase
from gitlab.tests.jsonschemas.user.schemas import\
    valid_schema, unauthorized_schema,\
    user_data_valid_schema, project_id_schema,\
    get_user_project_schema, user_id_schema
from jsonschema import validate
from gitlab.user.utils import UserUtils, send_message


class TestUser(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.user_utils = UserUtils(self.user.chat_id)

    def test_get_user_project(self):
        requested_user = self.user_utils.get_user_project()
        validate(requested_user, valid_schema)

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
        status = self.user_utils.send_button_message(user_data,
                                                     self.user.chat_id)
        self.assertIsInstance(status, str)

    def test_send_message(self):
        status = send_message(self.GITLAB_API_TOKEN, self.user.chat_id)
        self.assertIsInstance(status, str)

    def test_view_get_user_project(self):
        response = self.client.get("/user/{chat_id}/{project_owner}"
                                   .format(chat_id=self.user.chat_id,
                                           project_owner=self.user.gitlab_user)
                                   )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        validate(data, get_user_project_schema)

    def test_view_get_user_id(self):
        response = self.client.get("/user/id/{chat_id}/{project_owner}"
                                   .format(chat_id=self.user.chat_id,
                                           project_owner=self.user.gitlab_user)
                                   )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        validate(data, user_id_schema)

    def test_view_get_user_id_invalid_project_owner(self):
        project_owner = "wrong_user"
        response = self.client.get("/user/id/{chat_id}/{project_owner}"
                                   .format(chat_id=self.user.chat_id,
                                           project_owner=project_owner)
                                   )
        data = json.loads(response.data.decode())
        self.assertEqual(data["status_code"], 404)
        validate(data, unauthorized_schema)

    def test_view_get_project_id(self):
        response = self.client.get("/user/repo/{chat_id}/{project_owner}/"
                                   "{project_name}"
                                   .format(chat_id=self.user.chat_id,
                                           project_owner=self.user.gitlab_user,
                                           project_name=self.project.name)
                                   )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        validate(data, project_id_schema)

    def test_view_get_project_id_invalid_info(self):
        project_owner = "wrong_user"
        project_name = "wrong_project"
        response = self.client.get("/user/repo/{chat_id}/{project_owner}/"
                                   "{project_name}"
                                   .format(chat_id=self.user.chat_id,
                                           project_owner=project_owner,
                                           project_name=project_name)
                                   )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 404)
        validate(data, unauthorized_schema)


if __name__ == "__main__":
    unittest.main()
