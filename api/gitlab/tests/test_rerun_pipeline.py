import json
from gitlab.tests.base import BaseTestCase
from gitlab.tests.jsonschemas.rerun_pipeline.schemas import\
     rerun_pipeline_schema, unauthorized_schema

from jsonschema import validate
from gitlab.rerun_pipeline.utils import RerunPipeline
import os
from requests.exceptions import HTTPError


class TestRerunPipeline(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.rerun_pipeline = RerunPipeline(self.user.chat_id)

    def test_rerun_pipeline(self):
        pipeline_id = "63218612"
        response = self.rerun_pipeline.rerun_pipeline(self.project.project_id,
                                                      pipeline_id)
        validate(response, rerun_pipeline_schema)

    def test_rerun_pipeline_wrong_pipeline_id(self):
        pipeline_id = "6321861241"
        with self.assertRaises(HTTPError) as context:
            self.rerun_pipeline.rerun_pipeline(self.project.project_id,
                                               pipeline_id)
        unauthorized_json = json.loads(str(context.exception))
        self.assertTrue(unauthorized_json["status_code"], 404)
        validate(unauthorized_json, unauthorized_schema)

    def test_rerun_pipeline_invalid_token(self):
        self.user.access_token = "wrong_token"
        pipeline_id = "63218612"
        self.user.save()
        rerun_pipeline_invalid = RerunPipeline(self.user.chat_id)
        with self.assertRaises(HTTPError) as context:
            rerun_pipeline_invalid.rerun_pipeline(self.project.project_id,
                                                  pipeline_id)
        self.user.access_token = os.getenv("GITLAB_API_TOKEN", "")
        self.user.save()
        unauthorized_json = json.loads(str(context.exception))
        self.assertTrue(unauthorized_json["status_code"], 401)
        validate(unauthorized_json, unauthorized_schema)

    def test_build_buttons(self):
        pipeline_id = "63218612"
        buttons = self.rerun_pipeline.build_buttons(pipeline_id)
        self.assertIsInstance(buttons, list)

    def test_view_rerun_pipeline(self):
        pipeline_id = "63218612"
        response = self.client.get("/rerun_pipeline/{chat_id}/{pipeline_id}"
                                   .format(chat_id=self.user.chat_id,
                                           pipeline_id=pipeline_id))
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        validate(data, rerun_pipeline_schema)

    def test_view_rerun_pipeline_wrong_pipeline_id(self):
        pipeline_id = "632186121234"
        response = self.client.get("/rerun_pipeline/{chat_id}/{pipeline_id}"
                                   .format(chat_id=self.user.chat_id,
                                           pipeline_id=pipeline_id))
        invalid_project_json = json.loads(response.data.decode())
        self.assertTrue(invalid_project_json["status_code"], 404)
        validate(invalid_project_json, unauthorized_schema)
