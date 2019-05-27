import json
import unittest
from gitlab.tests.base import BaseTestCase
from gitlab.tests.jsonschemas.pipeline.schemas import\
     ping_schema, valid_schema, unauthorized_schema,\
     invalid_project_schema, pipeline_valid_schema,\
     pipeline_invalid_schema
from jsonschema import validate
from gitlab.pipeline.utils import Pipeline
from requests.exceptions import HTTPError
from gitlab.data.user import User
from gitlab.data import init_db
from gitlab.data.project import Project
import os


class TestPipeline(BaseTestCase):
    def setup(self):
        super().setUp()
        Project.drop_collection()
        User.drop_collection()

    def test_ping_pong(self):
        response = self.client.get("/pipeline/ping")
        data = json.loads(response.data.decode())
        ping_string = json.dumps(ping_schema)
        ping_json = json.loads(ping_string)
        self.assertEqual(response.status_code, 200)
        validate(data, ping_json)

    def test_view_get_project_pipeline(self):
        user = User()
        user.username = 'joaovitor'
        user.chat_id = '1234'
        user.gitlab_user = 'joaovitor3'
        user.gitlab_user_id = '1195203'
        user.save()
        project = Project()
        project_name = 'ada-gitlab'
        project_id = '11789629'
        project.save_webhook_infos(user, project_name, project_id)
        user.save_gitlab_repo_data(project)
        response = self.client.get("/pipeline/{chat_id}"
                                   .format(chat_id=user.chat_id))
        data = json.loads(response.data.decode())
        pipeline_string = json.dumps(pipeline_valid_schema)
        pipeline_json = json.loads(pipeline_string)
        self.assertEqual(response.status_code, 200)
        validate(data, pipeline_json)

    def test_view_get_project_pipeline_invalid_chat_id(self):
        chat_id = "8376"
        response = self.client.get("/pipeline/{chat_id}"
                                   .format(chat_id=chat_id))
        invalid_project_json = json.loads(response.data.decode())
        self.assertTrue(invalid_project_json["status_code"], 404)
        validate(invalid_project_json, pipeline_invalid_schema)

    def test_get_project_pipeline(self):
        GITLAB_API_TOKEN = os.getenv("GITLAB_API_TOKEN", "")
        pipeline = Pipeline(GITLAB_API_TOKEN)
        project_id = "11789629"
        requested_pipeline = pipeline.get_project_pipeline(project_id)
        validate(requested_pipeline, valid_schema)

    def test_get_project_pipeline_invalid_token(self):
        GITLAB_API_TOKEN = "wrong_token"
        pipeline = Pipeline(GITLAB_API_TOKEN)
        project_id = "11789629"
        with self.assertRaises(HTTPError) as context:
            pipeline.get_project_pipeline(project_id)
        unauthorized_json = json.loads(str(context.exception))
        self.assertTrue(unauthorized_json["status_code"], 401)
        validate(unauthorized_json, unauthorized_schema)

    def test_get_project_pipeline_invalid_project(self):
        GITLAB_API_TOKEN = os.getenv("GITLAB_API_TOKEN", "")
        pipeline = Pipeline(GITLAB_API_TOKEN)
        project_id = "wrong_name"
        with self.assertRaises(HTTPError) as context:
            pipeline.get_project_pipeline(project_id)
        invalid_project_json = json.loads(str(context.exception))
        self.assertTrue(invalid_project_json["status_code"], 404)
        validate(invalid_project_json, invalid_project_schema)


if __name__ == "__main__":
    unittest.main()
