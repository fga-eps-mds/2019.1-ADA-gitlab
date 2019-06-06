import json
from gitlab.tests.base import BaseTestCase
from gitlab.tests.jsonschemas.rerun_pipeline.schemas import\
     rerun_pipeline_schema, unauthorized_schema

from jsonschema import validate
from gitlab.rerun_pipeline.utils import RerunPipeline
from requests.exceptions import HTTPError
from unittest.mock import patch
from requests import Response


class TestRerunPipeline(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.rerun_pipeline = RerunPipeline(self.user.chat_id)
        self.mocked_valid_response = Response()
        mocked_content = {"id": 63218612,
                          "sha": "ab063122e7dfbf5172f6f75a052d72e1d1fd1af1",
                          "ref": "251-Mock",
                          "status": "running",
                          "web_url": "https://gitlab.com/"}
        content_in_binary = json.dumps(mocked_content).encode('utf-8')
        self.mocked_valid_response._content = content_in_binary
        self.mocked_valid_response.status_code = 200

    @patch('gitlab.rerun_pipeline.utils.post')
    def test_rerun_pipeline(self, mocked_post):
        pipeline_id = "63218612"
        mocked_post.return_value = self.mocked_valid_response
        response = self.rerun_pipeline.rerun_pipeline(self.project.project_id,
                                                      pipeline_id)
        validate(response, rerun_pipeline_schema)

    @patch('gitlab.utils.gitlab_utils.GitlabUtils.return_project')
    @patch('gitlab.utils.gitlab_utils.json')
    def test_rerun_pipeline_attribute_error(self, mocked_json, mocked_return_project):
        mocked_return_project.side_effect = AttributeError
        mocked_json.loads.return_value = {"status_code": 404}
        pipeline_id = "63218612"
        response = self.client.get("/rerun_pipeline/<chat_id>/<pipeline_id>"
                                   .format(chat_id=self.user.chat_id,
                                           pipeline_id=pipeline_id))
        invalid_project_json = json.loads(response.data.decode())
        self.assertTrue(invalid_project_json["status_code"], 404)
        validate(invalid_project_json, unauthorized_schema)

    @patch('gitlab.rerun_pipeline.utils.post')
    def test_rerun_pipeline_wrong_pipeline_id(self, mocked_post):
        pipeline_id = "9999999999"
        mocked_post.return_value = self.mocked_404_response
        with self.assertRaises(HTTPError) as context:
            self.rerun_pipeline.rerun_pipeline(self.project.project_id,
                                               pipeline_id)
        unauthorized_json = json.loads(str(context.exception))
        self.assertTrue(unauthorized_json["status_code"], 404)
        validate(unauthorized_json, unauthorized_schema)

    @patch('gitlab.rerun_pipeline.utils.post')
    @patch('gitlab.utils.gitlab_utils.GitlabUtils.get_access_token')
    def test_rerun_pipeline_invalid_token(self, mocked_access_token,
                                          mocked_post):
        mocked_access_token.return_value = "wrong_token"
        mocked_post.return_value = self.mocked_404_response
        pipeline_id = "63218612"
        rerun_pipeline_invalid = RerunPipeline(self.user.chat_id)
        with self.assertRaises(HTTPError) as context:
            rerun_pipeline_invalid.rerun_pipeline(self.project.project_id,
                                                  pipeline_id)
        unauthorized_json = json.loads(str(context.exception))
        self.assertTrue(unauthorized_json["status_code"], 401)
        validate(unauthorized_json, unauthorized_schema)

    def test_build_buttons(self):
        pipeline_id = "63218612"
        buttons = self.rerun_pipeline.build_buttons(pipeline_id)
        self.assertIsInstance(buttons, list)

    @patch('gitlab.rerun_pipeline.utils.post')
    def test_view_rerun_pipeline(self, mocked_post):
        mocked_post.return_value = self.mocked_valid_response
        pipeline_id = "63218612"
        response = self.client.get("/rerun_pipeline/{chat_id}/{pipeline_id}"
                                   .format(chat_id=self.user.chat_id,
                                           pipeline_id=pipeline_id))
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        validate(data, rerun_pipeline_schema)

    @patch('gitlab.rerun_pipeline.utils.post')
    def test_view_rerun_pipeline_wrong_pipeline_id(self, mocked_post):
        mocked_post.return_value = self.mocked_404_response
        pipeline_id = "632186121234"
        response = self.client.get("/rerun_pipeline/{chat_id}/{pipeline_id}"
                                   .format(chat_id=self.user.chat_id,
                                           pipeline_id=pipeline_id))
        invalid_project_json = json.loads(response.data.decode())
        self.assertTrue(invalid_project_json["status_code"], 404)
        validate(invalid_project_json, unauthorized_schema)
