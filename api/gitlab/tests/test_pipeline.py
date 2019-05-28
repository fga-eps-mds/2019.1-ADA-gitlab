import json
import unittest
from gitlab.tests.base import BaseTestCase
from gitlab.tests.jsonschemas.pipeline.schemas import\
     valid_schema, unauthorized_schema,\
     pipeline_valid_schema,\
     pipeline_invalid_schema
from jsonschema import validate
from gitlab.pipeline.pipeline_utils import Pipeline
from requests.exceptions import HTTPError
import os


class TestPipeline(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.pipeline = Pipeline(self.user.chat_id)

    def test_view_get_project_pipeline(self):
        response = self.client.get("/pipeline/{chat_id}"
                                   .format(chat_id=self.user.chat_id))
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

    def test_view_get_project_pipeline_invalid_token(self):
        self.user.access_token = "wrong_token"
        self.user.save()
        response = self.client.get("/pipeline/{chat_id}"
                                   .format(chat_id=self.user.chat_id))
        self.user.access_token = os.getenv("GITLAB_API_TOKEN", "")
        self.user.save()
        invalid_project_json = json.loads(response.data.decode())
        self.assertTrue(invalid_project_json["status_code"], 404)
        validate(invalid_project_json, pipeline_invalid_schema)

    def test_view_get_project_pipeline_invalid_project_id(self):
        self.project.project_id = "1234"
        self.project.save()
        response = self.client.get("/pipeline/{chat_id}"
                                   .format(chat_id=self.user.chat_id))
        self.project.project_id = "12532279"
        self.project.save()
        invalid_project_json = json.loads(response.data.decode())
        self.assertTrue(invalid_project_json["status_code"], 404)
        validate(invalid_project_json, pipeline_invalid_schema)

    def test_get_project_pipeline(self):
        requested_pipeline = self.pipeline.get_project_pipeline(
                                        self.project.project_id)
        validate(requested_pipeline, valid_schema)

    def test_get_project_pipeline_invalid_token(self):
        self.user.access_token = "wrong_token"
        self.user.save()
        wrong_pipeline = Pipeline(self.user.chat_id)
        with self.assertRaises(HTTPError) as context:
            wrong_pipeline.get_project_pipeline(self.project.project_id)
        self.user.access_token = os.getenv("GITLAB_API_TOKEN", "")
        self.user.save()
        unauthorized_json = json.loads(str(context.exception))
        self.assertTrue(unauthorized_json["status_code"], 401)
        validate(unauthorized_json, unauthorized_schema)

    def test_get_project_pipeline_no_pipeline(self):
        self.project.project_id = "12571001"
        self.project.save()
        wrong_pipeline = Pipeline(self.user.chat_id)
        with self.assertRaises(HTTPError) as context:
            wrong_pipeline.get_project_pipeline(self.project.project_id)
        self.project.project_id = "12532279"
        self.project.save()
        unauthorized_json = json.loads(str(context.exception))
        self.assertTrue(unauthorized_json["status_code"], 404)
        validate(unauthorized_json, unauthorized_schema)


if __name__ == "__main__":
    unittest.main()
