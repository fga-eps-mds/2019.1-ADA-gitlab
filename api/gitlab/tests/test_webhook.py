import json
from gitlab.tests.base import BaseTestCase
from gitlab.tests.jsonschemas.webhook.schemas import\
     message_error_schema, pipeline_schema,\
     build_messages_schema, views_schema
from jsonschema import validate
from gitlab.webhook.utils import Webhook
from requests.exceptions import HTTPError
from requests import Response
from unittest.mock import patch, Mock
from gitlab.data.user import User


class TestWebhook(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.webhook = Webhook()
        self.headers = {"Content-Type": "application/json",
                        "Authorization": "Bearer " + self.GITLAB_API_TOKEN}
        self.mocked_success_pipeline_response = Response()
        self.mocked_success_pipeline_response.status_code = 200
        self.success_pipeline_response_content = [{"id": 219564277,
                                                   "status": "success",
                                                   "stage": "test",
                                                   "name": "lint-flake8",
                                                   "ref": "300-AdaGitTest",
                                                   "commit": {
                                                    "short_id": "13a26c72",
                                                    "title": "#fix flake8 2",
                                                   },
                                                   "pipeline": {
                                                    "web_url":
                                                    "https://gitlab.com/"},
                                                   "web_url":
                                                   "https://gitlab.com/",
                                                   }]
        success_pipeline_response_content_in_binary = json.\
            dumps(self.success_pipeline_response_content).encode('utf-8')
        self.mocked_success_pipeline_response._content = \
            success_pipeline_response_content_in_binary

        self.gitlab_user = "adatestbot"
        self.gitlab_user_id = "4047441"
        self.user_data = {"gitlab_user": self.gitlab_user,
                          "chat_id": "12345689",
                          "gitlab_user_id": self.gitlab_user_id}

    def test_register_repo(self):
        user = self.user
        user.project = None
        user.save()
        user = User.objects(chat_id=self.user.chat_id).first()
        self.assertEqual(self.user.project, None)
        project_name = "ada-gitlab"
        project_id = "12532279"
        repo_data = {"project_name": project_name, "chat_id": "339847919",
                     "project_id": project_id}
        self.webhook.register_repo(repo_data)
        user = User.objects(chat_id=self.user.chat_id).first()
        self.assertEqual(user.project.name, project_name)
        self.assertEqual(user.project.project_id, project_id)

    def test_register_repo_http_error(self):
        repo_data = {"project_name": "ada-gitlab", "chat_id": "339847919",
                     "project_id": "12532279"}
        with self.assertRaises(HTTPError) as context:
            self.webhook.register_repo(repo_data)
        message_error = json.loads(str(context.exception))
        validate(message_error, message_error_schema)

    def test_register_user(self):
        self.webhook.register_user(self.user_data)
        user = User.objects(gitlab_user=self.gitlab_user).first()
        self.assertEqual(user.gitlab_user_id, self.gitlab_user_id)

    def test_register_user_again(self):
        new_user = self.user_data
        new_user["chat_id"] = "339847919"
        with self.assertRaises(HTTPError) as context:
            self.webhook.register_user(new_user)
        message_error = json.loads(str(context.exception))
        validate(message_error, message_error_schema)

    @patch('gitlab.webhook.utils.get')
    def test_get_pipeline_infos(self, mocked_get):
        mocked_get.return_value = self.mocked_success_pipeline_response
        pipeline_id = "63218612"
        pipeline_info = self.webhook.get_pipeline_infos(
                    self.project.project_id, pipeline_id)
        validate(pipeline_info[0], pipeline_schema)

    @patch('gitlab.webhook.utils.get')
    def test_build_messages_passed_pipeline(self, mocked_get):
        mocked_get.return_value = self.mocked_success_pipeline_response
        pipeline_id = "63226466"
        pipeline_info = self.webhook.get_pipeline_infos(
                    self.project.project_id, pipeline_id)
        build_messages = self.webhook.build_message(pipeline_info)
        validate(build_messages, build_messages_schema)

    @patch('gitlab.webhook.utils.get')
    def test_build_messages_failed_pipeline(self, mocked_get):
        mocked_failed_pipeline_response = self.mocked_success_pipeline_response
        failed_pipeline_response_content = \
            self.success_pipeline_response_content
        failed_pipeline_response_content[0]["status"] = "failed"
        failed_pipeline_response_content_in_binary = json.\
            dumps(failed_pipeline_response_content).encode('utf-8')
        mocked_failed_pipeline_response._content = \
            failed_pipeline_response_content_in_binary
        mocked_get.return_value = mocked_failed_pipeline_response

        pipeline_id = "63218612"
        pipeline_info = self.webhook.get_pipeline_infos(
                    self.project.project_id, pipeline_id)
        build_messages = self.webhook.build_message(pipeline_info)
        validate(build_messages, build_messages_schema)

    def test_view_register_user(self):
        response = self.client.post("/webhooks/user",
                                    data=json.dumps(self.user_data),
                                    headers=self.headers)
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        validate(data, views_schema)

    def test_view_register_repo(self):
        response = self.client.post("/webhooks/user",
                                    data=json.dumps(self.user_data),
                                    headers=self.headers)
        repo_data = {"project_name": "ada-gitlab", "chat_id": "12345689",
                     "project_id": "12532279"}
        response = self.client.post("/webhooks/repo",
                                    data=json.dumps(repo_data),
                                    headers=self.headers)
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        validate(data, views_schema)

    @patch('gitlab.webhook.views.Bot')
    @patch('gitlab.webhook.utils.get')
    def test_view_webhook_repository(self, mocked_get, mocked_bot):
        mocked_get.return_value = self.mocked_success_pipeline_response
        mocked_bot.return_value = Mock()
        mocked_bot.send_message = Mock()
        content_dict = {"object_kind": "pipeline",
                        "object_attributes":
                        {
                            "status": "success",
                            "id": "63218612",
                            "ref": "teste"
                            }
                        }
        content_json = json.dumps(content_dict)
        response = self.client.post(
                "/webhook/{chat_id}/{project_id}"
                .format(chat_id=self.user.chat_id,
                        project_id=self.project.project_id),
                data=content_json, headers=self.headers)
        self.assertEqual(response.status_code, 200)
