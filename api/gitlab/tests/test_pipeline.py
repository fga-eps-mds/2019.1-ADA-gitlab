import json
import unittest
from gitlab.tests.base import BaseTestCase
from gitlab.tests.jsonschemas.pipeline.schemas import\
     ping_schema, valid_schema, unauthorized_schema,\
     invalid_project_schema
from jsonschema import validate
from gitlab.pipeline.utils import Pipeline
from requests.exceptions import HTTPError
import os


class TestPipeline(BaseTestCase):
    def test_ping_pong(self):
        response = self.client.get("/pipeline/ping")
        data = json.loads(response.data.decode())
        ping_string = json.dumps(ping_schema)
        ping_json = json.loads(ping_string)
        self.assertEqual(response.status_code, 200)
        validate(data, ping_json)

    def test_get_project_pipeline(self):
        GITLAB_API_TOKEN = os.getenv("GITLAB_API_TOKEN", "")
        pipeline = Pipeline(GITLAB_API_TOKEN)
        project_owner = "gitlab-org"
        project_name = "gitlab-runner"
        requested_pipeline = pipeline.get_project_pipeline(project_owner,
                                                           project_name)
        validate(requested_pipeline, valid_schema)

    def test_get_project_pipeline_invalid_token(self):
        GITLAB_API_TOKEN = "wrong_token"
        pipeline = Pipeline(GITLAB_API_TOKEN)
        project_owner = "gitlab-org"
        project_name = "gitlab-runner"
        with self.assertRaises(HTTPError) as context:
            pipeline.get_project_pipeline(project_owner, project_name)
        unauthorized_json = json.loads(str(context.exception))
        self.assertTrue(unauthorized_json["status_code"], 401)
        validate(unauthorized_json, unauthorized_schema)

    def test_get_project_pipeline_invalid_project(self):
        GITLAB_API_TOKEN = os.getenv("GITLAB_API_TOKEN", "")
        pipeline = Pipeline(GITLAB_API_TOKEN)
        project_owner = "wrong_name"
        project_name = "gitlab-runner"
        with self.assertRaises(HTTPError) as context:
            pipeline.get_project_pipeline(project_owner, project_name)
        invalid_project_json = json.loads(str(context.exception))
        self.assertTrue(invalid_project_json["status_code"], 404)
        validate(invalid_project_json, invalid_project_schema)


if __name__ == "__main__":
    unittest.main()
