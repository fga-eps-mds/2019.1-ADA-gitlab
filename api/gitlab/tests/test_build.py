import json
import unittest
from gitlab.tests.base import BaseTestCase
from gitlab.tests.jsonschemas.build.schemas import\
    ping_schema, valid_schema, unauthorized_schema,\
    invalid_project_schema, build_valid_schema,\
    build_invalid_schema
from jsonschema import validate
from gitlab.build.utils import Build
from requests.exceptions import HTTPError
import os
import sys


class TestBuild(BaseTestCase):
    def test_ping_pong(self):
        response = self.client.get("/build/ping")
        data = json.loads(response.data.decode())
        ping_string = json.dumps(ping_schema)
        ping_json = json.loads(ping_string)
        self.assertEqual(response.status_code, 200)
        validate(data, ping_json)

    def test_view_get_project_build(self):
        project_owner = "gitlab-org"
        project_name = "gitlab-ee"
        response = self.client.get("/build/{project_owner}/{project_name}/jobs"
                                   .format(project_owner=project_owner,
                                           project_name=project_name))
        data = json.loads(response.data.decode())
        build_string = json.dumps(build_valid_schema)
        build_json = json.loads(build_string)
        self.assertEqual(response.status_code, 200)
        validate(data, build_json)

    def test_view_get_project_build_invalid_project(self):
        project_owner = "wrong_name"
        project_name = "gitlab-ee"
        response = self.client.get("/build/{project_owner}/{project_name}/jobs"
                                   .format(project_owner=project_owner,
                                           project_name=project_name))
        invalid_project_json = json.loads(response.data.decode())
        self.assertTrue(invalid_project_json["status_code"], 404)
        validate(invalid_project_json, build_invalid_schema)

    def test_get_project_build(self):
        GITLAB_API_TOKEN = os.getenv("GITLAB_API_TOKEN", "")
        print("TOKEN/n",file=sys.stderr)
        print(GITLAB_API_TOKEN, file=sys.stderr)
        build = Build(GITLAB_API_TOKEN)
        project_owner = "gitlab-org"
        project_name = "gitlab-ee"
        requested_build = build.get_project_build(project_owner,
                                                  project_name)
        validate(requested_build, valid_schema)

#     def test_get_project_build_invalid_token(self):
#         GITLAB_API_TOKEN = "wrong_token"
#         build = Build(GITLAB_API_TOKEN)
#         project_owner = "gitlab-org"
#         project_name = "gitlab-ee"
#         with self.assertRaises(HTTPError) as context:
#             build.get_project_build(project_owner, project_name)
#         unauthorized_json = json.loads(str(context.exception))
#         self.assertTrue(unauthorized_json["status_code"], 401)
#         validate(unauthorized_json, unauthorized_schema)

#     def test_get_project_build_invalid_project(self):
#         GITLAB_API_TOKEN = os.getenv("GITLAB_API_TOKEN", "")
#         build = Build(GITLAB_API_TOKEN)
#         project_owner = "wrong_name"
#         project_name = "gitlab-ee"
#         with self.assertRaises(HTTPError) as context:
#             build.get_project_build(project_owner, project_name)
#         invalid_project_json = json.loads(str(context.exception))
#         self.assertTrue(invalid_project_json["status_code"], 404)
#         validate(invalid_project_json, invalid_project_schema)


if __name__ == "__main__":
    unittest.main()
