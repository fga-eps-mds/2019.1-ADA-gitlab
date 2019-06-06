import json
from gitlab.tests.base import BaseTestCase
from gitlab.tests.jsonschemas.webhook.schemas import\
     message_error_schema, pipeline_schema,\
     build_messages_schema, views_schema
from jsonschema import validate
from gitlab.webhook.utils import Webhook
from requests.exceptions import HTTPError


class TestWebhook(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.webhook = Webhook(self.user.chat_id)
        self.headers = {"Content-Type": "application/json",
                        "Authorization": "Bearer " + self.GITLAB_API_TOKEN}

    def test_register_repo(self):
        old_project = self.user.project
        self.user.project = None
        self.user.save()
        repo_data = {"project_name": "ada-gitlab", "chat_id": "339847919",
                     "project_id": "12532279"}
        self.webhook.register_repo(repo_data)
        self.user.project = old_project
        self.user.save()

    def test_register_repo_http_error(self):
        repo_data = {"project_name": "ada-gitlab", "chat_id": "339847919",
                     "project_id": "12532279"}
        with self.assertRaises(HTTPError) as context:
            self.webhook.register_repo(repo_data)
        message_error = json.loads(str(context.exception))
        validate(message_error, message_error_schema)

    def test_register_user(self):
        user_data = {"gitlab_user": "adatestbot", "chat_id": "12345689",
                     "gitlab_user_id": "4047441"}
        self.webhook.register_user(user_data)

    def test_register_user_again(self):
        user_data = {"gitlab_user": "adatestbot", "chat_id": "339847919",
                     "gitlab_user_id": "4047441"}
        with self.assertRaises(HTTPError) as context:
            self.webhook.register_user(user_data)
        message_error = json.loads(str(context.exception))
        validate(message_error, message_error_schema)

    def test_get_pipeline_infos(self):
        pipeline_id = "63218612"
        pipeline_info = self.webhook.get_pipeline_infos(
                    self.project.project_id, pipeline_id)
        validate(pipeline_info[0], pipeline_schema)

    def test_build_messages_passed_pipeline(self):
        pipeline_id = "63226466"
        pipeline_info = self.webhook.get_pipeline_infos(
                    self.project.project_id, pipeline_id)
        build_messages = self.webhook.build_message(pipeline_info)
        validate(build_messages, build_messages_schema)

    def test_build_messages_failed_pipeline(self):
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

    def test_view_webhook_repository(self):
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
