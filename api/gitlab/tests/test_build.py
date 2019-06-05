import json
import unittest
from unittest.mock import patch
from gitlab.tests.base import BaseTestCase
from gitlab.tests.jsonschemas.build.schemas import\
    unauthorized_schema,\
    invalid_project_schema, build_valid_schema,\
    build_invalid_schema
from jsonschema import validate
from gitlab.build.build_utils import Build
from requests.exceptions import HTTPError
from requests import Response


class TestBuild(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.build = Build(self.user.chat_id)
        self.mocked_404_response = Response()
        self.mocked_404_response.status_code = 404
        self.mocked_401_response = Response()
        self.mocked_401_response.status_code = 401
        self.mocked_valid_response = Response()
        mocked_content = [{'id': 222325240,
                                      'status': 'success',
                                      'stage': 'test',
                                      'name': 'unit test',
                                      'ref': 'master',
                                      'commit':
                                      {'title': 'Merge PR',
                                       'short_id': '717b7ea7'},
                                      'pipeline':
                                      {'id': 63936796,
                                       'ref': 'master',
                                       'status': 'failed',
                                       'web_url':
                                       'https://gitlab.com/'},
                                      'web_url':
                                      'https://gitlab.com/',
                                      }]
        content_in_binary = json.dumps(mocked_content).encode('utf-8')
        self.mocked_valid_response._content = content_in_binary
        self.mocked_valid_response.status_code = 200

    @patch('gitlab.utils.gitlab_utils.get')
    def test_view_get_project_build(self, mocked_get):
        mocked_get.return_value = self.mocked_valid_response
        response = self.client.get("/build/{chat_id}"
                                   .format(chat_id=self.user.chat_id))
        data = json.loads(response.data.decode())
        build_string = json.dumps(build_valid_schema)
        build_json = json.loads(build_string)
        self.assertEqual(response.status_code, 200)
        validate(data, build_json)

    @patch('gitlab.utils.gitlab_utils.get')
    def test_view_get_project_build_invalid_project(self, mocked_get):
        mocked_get.return_value = self.mocked_404_response
        chat_id = "8212"
        response = self.client.get("/build/{chat_id}"
                                   .format(chat_id=chat_id))
        invalid_project_json = json.loads(response.data.decode())
        with self.assertRaises(HTTPError) as context:
            self.build.get_project_build(chat_id)
        unauthorized_json = json.loads(str(context.exception))
        self.assertTrue(unauthorized_json["status_code"], 404)
        validate(invalid_project_json, build_invalid_schema)

    @patch('gitlab.utils.gitlab_utils.get')
    def test_view_get_project_build_http_error(self, mocked_get):
        mocked_get.return_value = self.mocked_404_response
        chat_id = "8212"
        self.client.get("/build/{chat_id}".format(chat_id=chat_id))
        with self.assertRaises(HTTPError):
            self.build.get_project_build(chat_id)

    @patch('gitlab.utils.gitlab_utils.get')
    @patch('gitlab.utils.gitlab_utils.GitlabUtils.get_access_token')
    def test_view_get_project_build_invalid_token(self, mocked_access_token, mocked_get):
        mocked_get.return_value = self.mocked_401_response
        mocked_access_token.return_value = "wrong_token"
        response = self.client.get("/build/{chat_id}"
                                   .format(chat_id=self.user.chat_id))
        invalid_project_json = json.loads(response.data.decode())
        self.assertTrue(response.status_code, 401)
        validate(invalid_project_json, unauthorized_schema)

    @patch('gitlab.utils.gitlab_utils.get')
    def test_get_project_build(self, mocked_get):
        mocked_get.return_value = self.mocked_valid_response
        requested_build = self.build.get_project_build(self.project.project_id)
        validate(requested_build, build_valid_schema)

    @patch('gitlab.utils.gitlab_utils.get')
    @patch('gitlab.utils.gitlab_utils.GitlabUtils.get_access_token')
    def test_get_project_build_invalid_token(self, mocked_access_token, mocked_get):
        mocked_get.return_value = self.mocked_401_response
        mocked_access_token.return_value = "wrong_token"
        with self.assertRaises(HTTPError) as context:
            self.build.get_project_build(self.project.project_id)
        unauthorized_json = json.loads(str(context.exception))
        self.assertTrue(unauthorized_json["status_code"], 401)
        validate(unauthorized_json, unauthorized_schema)

    @patch('gitlab.utils.gitlab_utils.get')
    def test_get_project_build_invalid_project(self, mocked_get):
        mocked_get.return_value = self.mocked_404_response
        with self.assertRaises(HTTPError) as context:
            self.build.get_project_build("1234")
        invalid_project_json = json.loads(str(context.exception))
        self.assertTrue(invalid_project_json["status_code"], 404)
        validate(invalid_project_json, invalid_project_schema)


if __name__ == "__main__":
    unittest.main()
