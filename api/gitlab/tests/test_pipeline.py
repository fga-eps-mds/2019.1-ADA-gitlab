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
from requests import Response
from unittest.mock import patch


class TestPipeline(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.pipeline = Pipeline(self.user.chat_id)

    @patch('gitlab.pipeline.pipeline_utils.Pipeline.get_request')
    def test_view_get_project_pipeline(self, mocked_get_request):
        mocked_get_request.return_value = [{"id": 63936796,
                                            "sha": "717b7e",
                                            "ref": "master",
                                            "status": "failed",
                                            "web_url": "https://gitlab.com/"
                                            }]
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

    @patch('gitlab.utils.gitlab_utils.get')
    @patch('gitlab.utils.gitlab_utils.GitlabUtils.get_access_token')
    def test_view_get_project_pipeline_invalid_token(self, mocked_access_token,
                                                     mocked_get):
        mocked_access_token.return_value = "wrong_token"
        mocked_get.side_effect = HTTPError
        response = self.client.get("/pipeline/{chat_id}"
                                   .format(chat_id=self.user.chat_id))
        invalid_project_json = json.loads(response.data.decode())
        self.assertTrue(invalid_project_json["status_code"], 404)
        validate(invalid_project_json, pipeline_invalid_schema)

    @patch('gitlab.utils.gitlab_utils.get')
    @patch('gitlab.utils.gitlab_utils.User.get_user_project')
    def test_view_get_project_pipeline_invalid_project_id(self,
                                                          mocked_user_project,
                                                          mocked_get):
        mock_project = self.project
        mock_project.project_id = "1234"
        mocked_user_project.return_value = mock_project
        mocked_get.side_effect = HTTPError
        response = self.client.get("/pipeline/{chat_id}"
                                   .format(chat_id=self.user.chat_id))
        invalid_project_json = json.loads(response.data.decode())
        self.assertTrue(invalid_project_json["status_code"], 404)
        validate(invalid_project_json, pipeline_invalid_schema)

    @patch('gitlab.utils.gitlab_utils.get')
    @patch('gitlab.utils.gitlab_utils.User.get_user_project')
    def test_view_get_project_pipeline_invalid_project(self,
                                                       mocked_user_project,
                                                       mocked_get):
        mocked_get.side_effect = HTTPError
        mocked_user_project.return_value = None
        response = self.client.get("/pipeline/{chat_id}"
                                   .format(chat_id=self.user.chat_id))
        invalid_project_json = json.loads(response.data.decode())
        self.assertTrue(invalid_project_json["status_code"], 404)
        validate(invalid_project_json, pipeline_invalid_schema)

    @patch('gitlab.utils.gitlab_utils.get')
    def test_get_project_pipeline(self, mocked_get):
        mocked_response = Response()
        mocked_json_content = [{"id": 63936796,
                                "sha": "717b7e",
                                "ref": "master",
                                "status": "failed",
                                "web_url": "https://gitlab.com/"
                                }]
        content_in_binary = json.dumps(mocked_json_content).encode('utf-8')
        mocked_response._content = content_in_binary
        mocked_response.status_code = 200
        mocked_get.return_value = mocked_response
        requested_pipeline = self.pipeline.get_project_pipeline(
                                        self.project.project_id)
        validate(requested_pipeline, valid_schema)

    @patch('gitlab.utils.gitlab_utils.get')
    @patch('gitlab.utils.gitlab_utils.GitlabUtils.get_access_token')
    def test_get_project_pipeline_invalid_token(self, mocked_access_token,
                                                mocked_get):
        mocked_access_token.return_value = "wrong_token"
        mocked_get.side_effect = AttributeError
        wrong_pipeline = Pipeline(self.user.chat_id)
        with self.assertRaises(AttributeError) as context:
            wrong_pipeline.get_project_pipeline(self.project.project_id)
        unauthorized_json = json.loads(str(context.exception))
        self.assertTrue(unauthorized_json["status_code"], 401)
        validate(unauthorized_json, unauthorized_schema)

    @patch('gitlab.utils.gitlab_utils.GitlabUtils.get_request')
    def test_get_project_pipeline_no_pipeline(self, mocked_get_request):
        mocked_get_request.return_value = []
        wrong_pipeline = Pipeline(self.user.chat_id)
        with self.assertRaises(HTTPError) as context:
            wrong_pipeline.get_project_pipeline(self.project.project_id)
        unauthorized_json = json.loads(str(context.exception))
        self.assertTrue(unauthorized_json["status_code"], 404)
        validate(unauthorized_json, unauthorized_schema)


if __name__ == "__main__":
    unittest.main()
