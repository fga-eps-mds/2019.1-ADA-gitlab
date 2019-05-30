import json
from gitlab.tests.base import BaseTestCase
from gitlab.tests.jsonschemas.webhook.schemas import\
     message_error_schema, pipeline_schema,\
     build_messages_schema
from jsonschema import validate
from gitlab.webhook.utils import Webhook
from requests.exceptions import HTTPError


class TestWebhook(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.webhook = Webhook()

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

        # def test_build_status_message(self):
