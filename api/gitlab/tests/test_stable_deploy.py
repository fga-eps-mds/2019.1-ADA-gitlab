import json
from gitlab.tests.base import BaseTestCase
from jsonschema import validate
from gitlab.stable_deploy.stable_deploy_utils import StableDeploy
from unittest.mock import patch
from gitlab.tests.jsonschemas.stable_deploy.schemas import\
     stable_deploy_schema, invalid_project_schema
from requests.exceptions import HTTPError
from requests import Response


class TestStableDeploy(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.stable_deploy = StableDeploy(self.user.chat_id)
        self.mocked_post_response = Response()
        mocked_post_content = [
            {
                "post": "success"
            }
        ]
        mocked_post_content_in_binary = json.\
            dumps(mocked_post_content).encode('utf-8')
        self.mocked_post_response._content = mocked_post_content_in_binary
        self.mocked_post_response.status_code = 200

        self.mocked_get_response = Response()
        mocked_get_content = [
            {
                "status": "success",
                "id": 12345
            }
        ]
        mocked_get_content_in_binary = json.dumps(
            mocked_get_content).encode('utf-8')
        self.mocked_get_response._content = mocked_get_content_in_binary
        self.mocked_get_response.status_code = 200
        self.pipeline_id = 12345

    @patch('gitlab.stable_deploy.stable_deploy_utils.post')
    def test_utils_run_stable_deploy(self, mocked_post):
        mocked_post.return_value = self.mocked_post_response
        deploy_status = self.stable_deploy.run_stable_deploy(
            self.project_id, self.pipeline_id)
        validate(deploy_status, stable_deploy_schema)

    @patch('gitlab.stable_deploy.stable_deploy_utils.post')
    def test_utils_run_stable_deploy_wrong_project_id(self, mocked_post):
        mocked_post.return_value = self.mocked_404_response
        with self.assertRaises(HTTPError) as context:
            self.stable_deploy.run_stable_deploy(
                self.project_id, self.pipeline_id)
        invalid_project_id = json.loads(str(context.exception))
        self.assertTrue(invalid_project_id["status_code"], 404)
        validate(invalid_project_id, invalid_project_schema)

    @patch('gitlab.utils.gitlab_utils.get')
    def test_utils_find_latest_stable_version(self,
                                              mocked_get):
        mocked_get.return_value = self.mocked_get_response
        pipeline_id = self.stable_deploy.find_latest_stable_version(
                                        self.project_id)
        self.assertIsInstance(pipeline_id, int)

    @patch('gitlab.utils.gitlab_utils.get')
    def test_utils_find_latest_stable_version_wrong_project_id(
                    self, mocked_get):
        mocked_get.return_value = self.mocked_404_response
        with self.assertRaises(HTTPError) as context:
            self.stable_deploy.find_latest_stable_version(self.project_id)
        invalid_project_id = json.loads(str(context.exception))
        self.assertTrue(invalid_project_id["status_code"], 404)
        validate(invalid_project_id, invalid_project_schema)

    @patch('gitlab.utils.gitlab_utils.get')
    @patch('gitlab.stable_deploy.stable_deploy_utils.post')
    def test_views_stable_deploy(self, mocked_post,
                                 mocked_get):
        mocked_get.return_value = self.mocked_get_response
        mocked_post.return_value = self.mocked_post_response
        response = self.client.get("/stable_deploy/{chat_id}".format(
                                    chat_id=self.user.chat_id))
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        validate(data, stable_deploy_schema)

    @patch('gitlab.utils.gitlab_utils.get')
    @patch('gitlab.stable_deploy.stable_deploy_utils.post')
    def test_views_stable_deploy_invalid_project_id(self,
                                                    mocked_get,
                                                    mocked_post):
        mocked_get.return_value = self.mocked_404_response
        mocked_post.return_value = self.mocked_404_response
        response = self.client.get("/stable_deploy/{chat_id}".format(
                            chat_id=self.user.chat_id))
        data = json.loads(response.data.decode())
        stable_deploy_string = json.dumps(invalid_project_schema)
        stable_deploy_json = json.loads(stable_deploy_string)
        self.assertEqual(response.status_code, 404)
        validate(data, stable_deploy_json)

    def test_views_stable_deploy_invalid_chat_id(self):
        response = self.client.get("/stable_deploy/{chat_id}".format(
                            chat_id=None))

        data = json.loads(response.data.decode())
        stable_deploy_string = json.dumps(invalid_project_schema)
        stable_deploy_json = json.loads(stable_deploy_string)

        self.assertEqual(response.status_code, 404)
        validate(data, stable_deploy_json)
