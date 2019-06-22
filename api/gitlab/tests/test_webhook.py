import json
from gitlab.tests.base import BaseTestCase
from gitlab.tests.jsonschemas.webhook.schemas import\
     message_error_schema, pipeline_schema,\
     build_messages_schema, views_schema,\
     invalid_project_schema
from jsonschema import validate
from gitlab.webhook.utils import Webhook
from requests.exceptions import HTTPError
from requests import Response
from unittest.mock import patch, Mock
from gitlab.data.user import User
import sys


class TestWebhook(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.webhook = Webhook(self.user.chat_id)
        self.headers = {"Content-Type": "application/json",
                        "Authorization": "Bearer " + self.GITLAB_API_TOKEN}
        self.mocked_ok_pipeline_response = Response()
        self.mocked_ok_pipeline_response.status_code = 200
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
        self.mocked_ok_pipeline_response._content = \
            success_pipeline_response_content_in_binary

        self.mocked_failed_pipeline_response = Response()
        self.mocked_failed_pipeline_response.status_code = 200
        failed_pipeline_response_content = [{"id": 219564277,
                                             "status": "failed",
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
        failed_pipeline_response_content = \
            self.success_pipeline_response_content
        failed_pipeline_response_content[0]["status"] = "failed"
        failed_pipeline_response_content_in_binary = json.\
            dumps(failed_pipeline_response_content).encode('utf-8')
        self.mocked_failed_pipeline_response._content = \
            failed_pipeline_response_content_in_binary

        self.gitlab_user = "adatestbot"
        self.gitlab_user_id = "4047441"
        self.user_data = {"gitlab_user": self.gitlab_user,
                          "chat_id": "12345689",
                          "gitlab_user_id": self.gitlab_user_id}

        self.mocked_get_hooks_response = Response()
        self.mocked_get_hooks_response.status_code = 200
        sucess_mocked_get_hooks_response = [{"id": 123456789,
                                             "url": "https://gitlab." +
                                             "adachatops.com/"
                                             }]
        get_hooks_in_binary = json.\
            dumps(sucess_mocked_get_hooks_response).encode('utf-8')
        self.mocked_get_hooks_response._content = \
            get_hooks_in_binary

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

    @patch('gitlab.webhook.utils.os')
    @patch('gitlab.webhook.utils.delete')
    @patch('gitlab.webhook.utils.get')
    def test_register_repo_validation(self, mocked_get, mocked_delete,
                                      mocked_os):
        user = self.user
        user.save()
        user = User.objects(chat_id=self.user.chat_id).first()
        project_name = "ada-gitlab"
        project_id = "12532279"
        repo_data = {"project_name": project_name, "chat_id": "339847919",
                     "project_id": project_id}
        self.webhook.register_repo(repo_data)
        acess_token = "32y324798798732"
        webhook_url = "https://gitlab.adachatops.com/"
        mocked_os.getenv.return_value = acess_token
        mocked_os.getenv.return_value = webhook_url
        delete_hook = Response()
        delete_hook.status_code = 200
        mocked_get.return_value = self.mocked_get_hooks_response
        mocked_delete.return_value = delete_hook
        user = User.objects(chat_id=self.user.chat_id).first()
        self.assertEqual(user.project.name, project_name)
        self.assertEqual(user.project.project_id, project_id)

    @patch('gitlab.webhook.utils.get')
    def test_register_repo_http_error(self, mocked_get):
        project_name = "ada-gitlab"
        project_id = "12532279"
        repo_data = {"project_name": project_name, "chat_id": "sasa",
                     "project_id": project_id}
        mocked_get.return_value = self.mocked_404_response
        with self.assertRaises(HTTPError) as context:
            self.webhook.register_repo(repo_data)
        print(self.webhook.register_repo, file=sys.stderr)
        message_error = json.loads(str(context.exception))
        validate(message_error, invalid_project_schema)

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
        mocked_get.return_value = self.mocked_ok_pipeline_response
        pipeline_id = "63218612"
        pipeline_info = self.webhook.get_pipeline_infos(
                    self.project.project_id, pipeline_id)
        validate(pipeline_info[0], pipeline_schema)

    @patch('gitlab.webhook.utils.get')
    def test_build_messages_passed_pipeline(self, mocked_get):
        mocked_get.return_value = self.mocked_ok_pipeline_response
        pipeline_id = "63226466"
        pipeline_info = self.webhook.get_pipeline_infos(
                    self.project.project_id, pipeline_id)
        build_messages = self.webhook.build_message(pipeline_info)
        validate(build_messages, build_messages_schema)

    @patch('gitlab.webhook.utils.get')
    def test_build_messages_failed_pipeline(self, mocked_get):
        mocked_get.return_value = self.mocked_failed_pipeline_response

        pipeline_id = "63218612"
        pipeline_info = self.webhook.get_pipeline_infos(
                    self.project.project_id, pipeline_id)
        build_messages = self.webhook.build_message(pipeline_info)
        validate(build_messages, build_messages_schema)

    @patch('gitlab.webhook.utils.get')
    def test_build_messages_running_pipeline(self, mocked_get):
        mocked_running_pipeline_response = self.\
            mocked_ok_pipeline_response
        running_pipeline_response_content = \
            self.success_pipeline_response_content
        running_pipeline_response_content[0]["status"] = "running"
        running_pipeline_response_content_in_binary = json.\
            dumps(running_pipeline_response_content).encode('utf-8')
        mocked_running_pipeline_response._content = \
            running_pipeline_response_content_in_binary
        mocked_get.return_value = mocked_running_pipeline_response

        pipeline_id = "63218612"
        pipeline_info = self.webhook.get_pipeline_infos(
                    self.project.project_id, pipeline_id)
        build_messages = self.webhook.build_message(pipeline_info)
        validate(build_messages, build_messages_schema)

    def test_view_register_repo(self):
        self.user.project = None
        self.user.save()
        repo_data = {"project_name": "ada-gitlab", "chat_id": "339847919",
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
        mocked_get.return_value = self.mocked_ok_pipeline_response
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

    @patch('gitlab.webhook.views.Bot')
    @patch('gitlab.webhook.utils.get')
    def test_view_webhook_failed_repository(self, mocked_get, mocked_bot):
        mocked_get.return_value = self.mocked_failed_pipeline_response
        mocked_bot.return_value = Mock()
        mocked_bot.send_message = Mock()
        content_dict = {"object_kind": "pipeline",
                        "object_attributes":
                        {
                            "status": "failed",
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

    @patch('gitlab.webhook.views.request')
    @patch('gitlab.webhook.utils.post')
    def test_view_set_webhook(self, mocked_post, mocked_request):
        mocked_request.get_json.return_value = {
                        "project_id": "9121",
                        "chat_id": "12345689"
        }
        content_dict = {"id": 814315,
                        "url": "https://gitlab.adachatops.com/",
                        "push_events": True,
                        "project_id": 11789629,
                        }
        content_json = json.dumps(content_dict)
        mocked_response = Response()
        mocked_response.status_code = 200
        mocked_response._content = content_json
        mocked_post.return_value = mocked_response
        self.webhook.register_user(self.user_data)
        response = self.client.post("/webhook",
                                    data=content_json,
                                    headers=self.headers)
        self.assertEqual(response.status_code, 200)

    @patch('gitlab.webhook.utils.post')
    def test_view_invalid_set_webhook(self, mocked_post):
        mocked_post.return_value = Response()
        mocked_post.status_code = 400
        content_dict = {
                        "project_id": "9121",
                        "chat_id": "12345689"
        }
        content_json = json.dumps(content_dict)
        response = self.client.post("/webhook",
                                    data=content_json,
                                    headers=self.headers)
        self.assertEqual(response.status_code, 400)

    @patch('gitlab.webhook.utils.os')
    @patch('gitlab.webhook.utils.delete')
    @patch('gitlab.webhook.utils.get')
    def test_delete_webhook(self, mocked_get, mocked_delete,
                            mocked_os):
        project_id = 9121
        acess_token = "32y324798798732"
        webhook_url = "https://gitlab.adachatops.com/"
        mocked_os.getenv.return_value = acess_token
        mocked_os.getenv.return_value = webhook_url
        delete_hook = Response()
        delete_hook.status_code = 200
        mocked_get.return_value = self.mocked_get_hooks_response
        mocked_delete.return_value = delete_hook
        self.webhook.delete_webhook(project_id)
