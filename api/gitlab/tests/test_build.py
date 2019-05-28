import json
import unittest
from gitlab.tests.base import BaseTestCase
from gitlab.tests.jsonschemas.build.schemas import\
    ping_schema, valid_schema, unauthorized_schema,\
    invalid_project_schema, build_valid_schema,\
    build_invalid_schema
from jsonschema import validate
from gitlab.build.build_utils import Build
from gitlab.data.user import User
from gitlab.data.project import Project
import os
import sys
from requests.exceptions import HTTPError



class TestBuild(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.build = Build(self.user.chat_id)

    def test_view_get_project_build(self):
        response = self.client.get("/build/{chat_id}"
                                   .format(chat_id=self.user.chat_id))
        data = json.loads(response.data.decode())
        build_string = json.dumps(build_valid_schema)
        build_json = json.loads(build_string)
        self.assertEqual(response.status_code, 200)
        validate(data, build_json)

    def test_view_get_project_build_invalid_project(self):
        chat_id = "8212"
        response = self.client.get("/build/{chat_id}"
                                   .format(chat_id=chat_id))
        invalid_project_json = json.loads(response.data.decode())
        with self.assertRaises(HTTPError) as context:
            self.build.get_project_build(chat_id)
        unauthorized_json = json.loads(str(context.exception))
        self.assertTrue(unauthorized_json["status_code"], 404)
        validate(invalid_project_json, build_invalid_schema)
    
    def test_view_get_project_build_invalid_token(self):
        self.user.access_token = "wrong_token"
        self.user.save()
        response = self.client.get("/build/{chat_id}"
                                   .format(chat_id=self.user.chat_id))
        self.user.access_token = os.getenv("GITLAB_API_TOKEN", "")
        self.user.save()
        invalid_project_json = json.loads(response.data.decode())
        self.assertTrue(response.status_code, 401)
        validate(invalid_project_json, unauthorized_schema)

    def test_get_project_build(self):
        requested_build = self.build.get_project_build(self.project.project_id)
        validate(requested_build, valid_schema)

    def test_get_project_build_invalid_token(self):
        self.user.access_token = "wrong_token"
        self.user.save()
        with self.assertRaises(HTTPError) as context:
            self.build.get_project_build(self.project.project_id)
        unauthorized_json = json.loads(str(context.exception))
        self.user.access_token = os.getenv("GITLAB_API_TOKEN", "")
        self.user.save()
        self.assertTrue(unauthorized_json["status_code"], 401)
        validate(unauthorized_json, unauthorized_schema)

    def test_get_project_build_invalid_project(self):
        with self.assertRaises(HTTPError) as context:
            self.build.get_project_build("1234")
        invalid_project_json = json.loads(str(context.exception))
        self.assertTrue(invalid_project_json["status_code"], 404)
        validate(invalid_project_json, invalid_project_schema)


if __name__ == "__main__":
    unittest.main()
