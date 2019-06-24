import json
import unittest
from gitlab.tests.base import BaseTestCase
from gitlab.tests.jsonschemas.user.schemas import\
    unauthorized_schema,\
    user_data_valid_schema, project_id_schema,\
    user_id_schema, get_user_domain_schema,\
    save_user_domain_schema, user_invalid_schema,\
    get_user_infos_schema, get_repo_full_name_shcema
from jsonschema import validate
from gitlab.user.utils import UserUtils, send_message
from requests import Response
from unittest.mock import patch, Mock
from gitlab.user.utils import authenticate_access_token


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
        self.get_user_project_response_content = [{"id": "12571001",
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

        self.mocked_get_user_domain_response = Response()
        self.mocked_get_user_domain_response.status_code = 200
        get_user_domain_response_content = [{"chat_id": 360396695,
                                             "domain":
                                             "https://www.youtube.com.br"
                                             }]
        get_user_domain_content_in_binary = json.\
            dumps(get_user_domain_response_content).encode('utf-8')
        self.mocked_get_user_domain_response._content = \
            get_user_domain_content_in_binary

        get_repo_content = [
            {
                "name": "mocked_user",
                "path_with_namespace": "mocked_user/mocked_repo",
                "id": 123456
            }
        ]
        get_repo_content_in_binary = json.dumps(get_repo_content).\
            encode('utf-8')
        self.mocked_valid_get_repo = Response()
        self.mocked_valid_get_repo._content = get_repo_content_in_binary
        self.mocked_valid_get_repo.status_code = 200
        get_own_data_content = {
            "username": "mocked_user",
            "id": "123456789"
        }
        get_own_data_content_in_binary = json.dumps(
            get_own_data_content).encode('utf-8')
        self.mocked_valid_own_data = Response()
        self.mocked_valid_own_data._content = get_own_data_content_in_binary
        self.mocked_valid_own_data.status_code = 200
        mocked_post_content = {
            "access_token": "xyz789abc123"
        }
        mocked_post_content_in_binary = json.dumps(mocked_post_content).\
            encode('utf-8')
        self.mocked_post_valid = Response()
        self.mocked_post_valid._content = mocked_post_content_in_binary
        self.mocked_post_valid.status_code = 200

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
        mocked_get.side_effect = (self.mocked_get_user_project_response,
                                  self.mocked_get_user_id_response)
        buttons = self.user_utils.select_repos_by_buttons()
        self.assertIsInstance(buttons, list)

    @patch('gitlab.utils.gitlab_utils.get')
    @patch('gitlab.user.utils.Bot')
    def test_send_button_message(self, mocked_bot, mocked_get):
        mocked_get.side_effect = (self.mocked_get_user_data_response,
                                  self.mocked_get_user_project_response,
                                  self.mocked_get_user_id_response)
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

    @patch('gitlab.utils.gitlab_utils.get')
    def test_view_get_user_domain(self, mocked_get):
        mocked_get.return_value = self.mocked_get_user_domain_response
        response = self.client.get("/user/{chat_id}/domain"
                                   .format(chat_id=self.user.chat_id)
                                   )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        validate(data, get_user_domain_schema)

    @patch('gitlab.utils.gitlab_utils.get')
    def test_view_get_user_domain_invalid_information(self, mocked_get):
        mocked_get.return_value = self.mocked_get_user_domain_response

        chat_id = "wrong_chat_id"
        response = self.client.get("/user/{chat_id}/domain"
                                   .format(chat_id=chat_id)
                                   )
        data = json.loads(response.data.decode())
        self.assertEqual(data["status_code"], 404)
        validate(data, unauthorized_schema)

    def test_view_save_user_domain(self):
        url_domain = {"domain": "https://www.google.com.br"}
        headers = {'Content-Type': 'application/json'}
        response = self.client.post("/user/domain/{chat_id}"
                                    .format(chat_id=self.user.chat_id),
                                    data=json.dumps(url_domain),
                                    headers=headers
                                    )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        validate(data, save_user_domain_schema)

    def test_view_save_user_domain_invalid_info(self):
        chat_id = "Wrong chat id"
        url_domain = {"domain": "https://www.google.com.br"}
        headers = {'Content-Type': 'application/json'}
        response = self.client.post("/user/domain/{chat_id}"
                                    .format(chat_id=chat_id),
                                    data=json.dumps(url_domain),
                                    headers=headers
                                    )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 404)
        validate(data, user_invalid_schema)

    @patch('gitlab.user.views.request')
    @patch('gitlab.user.utils.Bot')
    def test_get_access_token(self, mocked_bot, mocked_request):
        mocked_bot.return_value = Mock()
        mocked_bot.send_message = Mock()
        code = "h3464kdi883"
        state = self.user.chat_id
        mocked_request.args.get.side_effect = (code, state)
        response = self.client.get("/user/gitlab/authorize")
        self.assertEqual(response.status_code, 302)

    @patch('gitlab.user.views.request')
    @patch('gitlab.user.utils.Bot')
    @patch('gitlab.user.views.authenticate_access_token')
    @patch('gitlab.utils.gitlab_utils.get')
    def test_get_access_token_non_existing_user(self, mocked_get,
                                                mocked_auth_access_token,
                                                mocked_bot,
                                                mocked_request):
        mocked_get.side_effect = (self.mocked_get_user_data_response,
                                  self.mocked_get_user_project_response,
                                  self.mocked_get_user_id_response)
        mocked_auth_access_token.return_value = "9a3506fced2455e52fe1ac48d"
        mocked_bot.return_value = Mock()
        mocked_bot.send_message = Mock()
        code = "h3464kdi883"
        state = "229247912"
        mocked_request.args.get.side_effect = (code, state)
        response = self.client.get("/user/gitlab/authorize")
        self.assertEqual(response.status_code, 302)

    @patch('gitlab.user.utils.post')
    def test_authenticate_access_token(self, mocked_post):
        mocked_response = Response()
        mocked_content = {"access_token": "6321861256"}
        content_in_binary = json.dumps(mocked_content).encode('utf-8')
        mocked_response._content = content_in_binary
        mocked_response.status_code = 200
        mocked_post.return_value = mocked_response
        authenticate_access_token("44456")

    def test_views_get_user_infos(self):
        chat_id = self.user.chat_id
        response = self.client.get("/user/infos/{chat_id}"
                                   .format(chat_id=chat_id))
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        validate(data, get_user_infos_schema)

    @patch('gitlab.utils.gitlab_utils.get')
    def test_views_get_project_fullname(self, mocked_get):
        mocked_get_user_project_response = Response()
        mocked_get_user_project_response.status_code = 200
        get_user_project_response_content = {"id": self.project.project_id,
                                             "path_with_namespace":
                                             "adatestbot/ada"}
        get_user_project_content_in_binary = json.\
            dumps(get_user_project_response_content).encode('utf-8')
        mocked_get_user_project_response._content = \
            get_user_project_content_in_binary
        mocked_get.return_value = mocked_get_user_project_response
        response = self.client.get("/user/project/{chat_id}/{project_id}"
                                   .format(chat_id=self.user.chat_id,
                                           project_id=self.project.project_id))
        data = json.loads((response.data.decode()))
        self.assertEqual(response.status_code, 200)
        validate(data, get_repo_full_name_shcema)

    @patch('gitlab.utils.gitlab_utils.get')
    def test_views_get_project_fullname_invalid(self, mocked_get):
        mocked_get.return_value = self.mocked_404_response
        response = self.client.get("/user/project/{chat_id}/{project_id}"
                                   .format(chat_id=self.user.chat_id,
                                           project_id=self.project.project_id))
        data = json.loads(response.data.decode())
        self.assertEqual(data["status_code"], 404)
        validate(data, unauthorized_schema)

    @patch('gitlab.user.utils.Bot')
    @patch('gitlab.utils.gitlab_utils.get')
    def test_view_change_repository_gitlab(self, mocked_get, mocked_bot):
        mocked_get.side_effect = (self.mocked_valid_own_data,
                                  self.mocked_valid_get_repo)
        mocked_bot.return_value = Mock()
        mocked_bot.send_message = Mock()
        response = self.client.get("/user/change_repo_gitlab/{chat_id}"
                                   .format(chat_id=self.user.chat_id))
        self.assertEqual(response.status_code, 200)

    @patch('gitlab.user.utils.Bot')
    @patch('gitlab.utils.gitlab_utils.get')
    def test_view_change_repository_gitlab_invalid(self, mocked_get,
                                                   mocked_bot):
        mocked_get.return_value = self.response_unauthorized
        mocked_bot.return_value = Mock()
        mocked_bot.send_message = Mock()
        response = self.client.get("/user/change_repo_gitlab/{chat_id}"
                                   .format(chat_id=self.user.chat_id))
        self.assertEqual(response.status_code, 401)


if __name__ == "__main__":
    unittest.main()
