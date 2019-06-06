import json
import unittest
from gitlab.tests.base import BaseTestCase
from gitlab.tests.jsonschemas.user.schemas import\
    valid_schema, unauthorized_schema,\
    user_data_valid_schema, project_id_schema,\
    get_user_project_schema, user_id_schema
from jsonschema import validate
from gitlab.user.utils import UserUtils, send_message
from requests.exceptions import HTTPError
from requests import Response
from unittest.mock import patch, Mock


class TestUser(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.user_utils = UserUtils(self.user.chat_id)

        self.mocked_get_user_id_response = Response()
        self.mocked_get_user_id_response.status_code = 200
        get_user_id_response_content = [{"id": 4047441,
                                         "name": "Ada Lovelace",
                                         "username": "adatestbot",
                                         "state": "active"
                                         }]
        get_user_id_content_in_binary = json.\
            dumps(get_user_id_response_content).encode('utf-8')
        self.mocked_get_user_id_response._content = \
            get_user_id_content_in_binary

        self.mocked_get_user_project_response = Response()
        self.mocked_get_user_project_response.status_code = 200
        self.get_user_project_response_content = [{"id": 12571001,
                                                   "name": "Ada",
                                                   "name_with_namespace":
                                                   "Ada Lovelace / Ada",
                                                   "path": "ada",
                                                   "path_with_namespace":
                                                   "adatestbot/ada"}]
        get_user_project_content_in_binary = json.\
            dumps(self.get_user_project_response_content).encode('utf-8')
        self.mocked_get_user_project_response._content = \
            get_user_project_content_in_binary

        self.mocked_get_user_data_response = Response()
        self.mocked_get_user_data_response.status_code = 200
        get_user_data_content = {"id": 4047441,
                                 "name": "Ada Lovelace",
                                 "username": "adatestbot",
                                 "state": "active"}
        get_user_data_content_in_binary = json.\
            dumps(get_user_data_content).encode('utf-8')
        self.mocked_get_user_data_response._content = \
            get_user_data_content_in_binary

        self.mocked_invalid_get_user_id_response = Response()
        self.mocked_invalid_get_user_id_response.status_code = 200
        invalid_get_user_id_response_content = []
        invalid_get_user_id_content_in_binary = json.\
            dumps(invalid_get_user_id_response_content).encode('utf-8')
        self.mocked_invalid_get_user_id_response._content = \
            invalid_get_user_id_content_in_binary

    @patch('gitlab.utils.gitlab_utils.get')
    def test_get_user_project(self, mocked_get):
        mocked_get.side_effect = (self.mocked_get_user_id_response,
                                  self.mocked_get_user_project_response)
        requested_user = self.user_utils.get_user_project(
                                self.user.gitlab_user)
        validate(requested_user, valid_schema)

    @patch('gitlab.utils.gitlab_utils.get')
    def test_get_user_project_invalid_user(self, mocked_get):
        mocked_get.return_value = self.mocked_invalid_get_user_id_response
        invalid_user = "wrong_user"
        with self.assertRaises(HTTPError) as context:
            self.user_utils.get_user_project(invalid_user)
        unauthorized_json = json.loads(str(context.exception))
        self.assertTrue(unauthorized_json["status_code"], 404)
        validate(unauthorized_json, unauthorized_schema)

    @patch('gitlab.utils.gitlab_utils.get')
    def test_get_user_id(self, mocked_get):
        mocked_get.return_value = self.mocked_get_user_id_response
        user_id = self.user_utils.get_user_id(self.user.gitlab_user)
        self.assertIsInstance(user_id, int)

    @patch('gitlab.utils.gitlab_utils.get')
    def test_get_own_user_data(self, mocked_get):
        mocked_get.return_value = self.mocked_get_user_data_response
        user_data = self.user_utils.get_own_user_data()
        validate(user_data, user_data_valid_schema)

    @patch('gitlab.utils.gitlab_utils.get')
    def test_select_repos_by_buttons(self, mocked_get):
        mocked_get.side_effect = (self.mocked_get_user_id_response,
                                  self.mocked_get_user_project_response)
        buttons = self.user_utils.select_repos_by_buttons(
                                    self.user.gitlab_user)
        self.assertIsInstance(buttons, list)

    @patch('gitlab.utils.gitlab_utils.get')
    @patch('gitlab.user.utils.Bot')
    def test_send_button_message(self, mocked_bot, mocked_get):
        mocked_get.side_effect = (self.mocked_get_user_data_response,
                                  self.mocked_get_user_id_response,
                                  self.mocked_get_user_project_response)
        mocked_bot.return_value = Mock()
        mocked_bot.send_message = Mock()
        user_data = self.user_utils.get_own_user_data()
        status = self.user_utils.send_button_message(user_data,
                                                     self.user.chat_id)
        self.assertIsInstance(status, str)

    @patch('gitlab.user.utils.Bot')
    def test_send_message(self, mocked_bot):
        mocked_bot.return_value = Mock()
        mocked_bot.send_message = Mock()
        status = send_message(self.GITLAB_API_TOKEN, self.user.chat_id)
        self.assertEqual(status, "OK")

    @patch('gitlab.utils.gitlab_utils.get')
    def test_view_get_user_project(self, mocked_get):
        mocked_get.side_effect = (self.mocked_get_user_id_response,
                                  self.mocked_get_user_project_response)
        response = self.client.get("/user/{chat_id}/{project_owner}"
                                   .format(chat_id=self.user.chat_id,
                                           project_owner=self.user.gitlab_user)
                                   )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        validate(data, get_user_project_schema)

    @patch('gitlab.utils.gitlab_utils.get')
    def test_view_get_user_project_blank_project_owner(self, mocked_get):
        mocked_get.return_value = self.mocked_404_response
        response = self.client.get("/user/{chat_id}/{project_owner}"
                                   .format(chat_id=self.user.chat_id,
                                           project_owner=None)
                                   )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 404)
        validate(data, unauthorized_schema)

    @patch('gitlab.utils.gitlab_utils.get')
    def test_view_get_user_project_invalid_project_owner(self, mocked_get):
        mocked_get.return_value = self.mocked_404_response
        project_owner = "wrong_user"
        response = self.client.get("/user/{chat_id}/{project_owner}"
                                   .format(chat_id=self.user.chat_id,
                                           project_owner=project_owner)
                                   )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 404)
        validate(data, unauthorized_schema)

    @patch('gitlab.utils.gitlab_utils.get')
    def test_view_get_user_id(self, mocked_get):
        mocked_get.return_value = self.mocked_get_user_id_response
        response = self.client.get("/user/id/{chat_id}/{project_owner}"
                                   .format(chat_id=self.user.chat_id,
                                           project_owner=self.user.gitlab_user)
                                   )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        validate(data, user_id_schema)

    @patch('gitlab.utils.gitlab_utils.get')
    def test_view_get_user_id_invalid_project_owner(self, mocked_get):
        mocked_get.return_value = self.mocked_invalid_get_user_id_response

        project_owner = "wrong_user"
        response = self.client.get("/user/id/{chat_id}/{project_owner}"
                                   .format(chat_id=self.user.chat_id,
                                           project_owner=project_owner)
                                   )
        data = json.loads(response.data.decode())
        self.assertEqual(data["status_code"], 404)
        validate(data, unauthorized_schema)

    @patch('gitlab.utils.gitlab_utils.get')
    def test_view_get_project_id(self, mocked_get):
        mocked_response = self.mocked_get_user_project_response
        response_content = self.get_user_project_response_content[0]
        response_content_in_binary = json.\
            dumps(response_content).encode('utf-8')
        mocked_response._content = response_content_in_binary
        mocked_get.return_value = mocked_response

        response = self.client.get("/user/repo/{chat_id}/{project_owner}/"
                                   "{project_name}"
                                   .format(chat_id=self.user.chat_id,
                                           project_owner=self.user.gitlab_user,
                                           project_name=self.project.name)
                                   )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        validate(data, project_id_schema)

    @patch('gitlab.utils.gitlab_utils.get')
    def test_view_get_project_id_invalid_info(self, mocked_get):
        mocked_get.return_value = self.mocked_404_response
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
