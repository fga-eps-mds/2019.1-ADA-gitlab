import json
from gitlab.tests.base import BaseTestCase
from jsonschema import validate
from gitlab.stable_deploy.utils import StableDeploy
import os
from gitlab.data.user import User
from gitlab.data import init_db
from gitlab.data.project import Project
from gitlab.tests.jsonschemas.stable_deploy.schemas import\
    ping_schema, stable_deploy_schema
from requests.exceptions import HTTPError
import sys

class TestStableDeploy(BaseTestCase):
    GITLAB_API_TOKEN = os.getenv("GITLAB_API_TOKEN", "")

    def setup(self):
        init_db()
        Project.drop_collection()
        User.drop_collection()

#    # casos felizes
#
#    def test_stable_deploy_utils_run_stable_deploy(self):
#        # error 403
#        pipeline_id = "62395673" # Ada-gitlab -> pipeline falhou
#        project_id = "11754240"  # Ada-gitlab
#        stable_deploy = StableDeploy(self.GITLAB_API_TOKEN)
#        response = stable_deploy.run_stable_deploy(project_id,
#                                                pipeline_id)
#        validate(response, stable_deploy_schema)
#
#
#    def test_stable_deploy_utils_find_latest_stable_version(self):
#        project_id = "11754240" # Ada-gitlab
#        stable_deploy = StableDeploy(self.GITLAB_API_TOKEN)
#        pipeline_id = stable_deploy.find_latest_stable_version(project_id)
#        self.assertIsInstance(pipeline_id, int)
#
    def test_stable_deploy_views_ping_pong(self):
        response = self.client.get("/stable_deploy/ping")
        data = json.loads(response.data.decode())
        ping_string = json.dumps(ping_schema)
        ping_json = json.loads(ping_string)
        self.assertEqual(response.status_code, 200)
        validate(data, ping_json)
#
#
    def test_stable_deploy_views_stable_deploy(self):
        pipeline_id = "62395673" # Ada-gitlab -> pipeline falhou
        chat_id = "123456789"
        user = User()
        user.create_user("sudjoao")
        user.chat_id = chat_id
        project = Project()
        project.create_project(user, "abc", "ada_gitlab",
                               "https://gitlab.com/sudjoao/ada-gitlab/", [],
                               "11754240")
        user.project = project
        user.save()
        # Testar
        response = self.client.get("/stable_deploy/{chat_id}/"
                                   .format(chat_id=chat_id))
        User.delete(user)

        print("\n\n\n\n\n\n\n", file=sys.stderr)
        print(response)
        print("\n\n\n\n\n\n\n")

        validate(response, stable_deploy_schema)
#
#    # casos tristes
#    def test_stable_deploy_utils_run_stable_deploy_ERROR(self):
#        pipeline_id = "00000321"
#        project_id = "000000123"
#        stable_deploy = StableDeploy(self.GITLAB_API_TOKEN)
#        with self.assertRaises(HTTPError) as context:
#            stable_deploy.run_stable_deploy(project_id, pipeline_id)
#        unauthorized_json = json.loads(str(context.exception))
#        self.assertTrue(unauthorized_json["status_code"], 404)
#
#    def test_stable_deploy_utils_find_latest_stable_version_ERROR(self):
#        project_id = "00000321"
#        stable_deploy = StableDeploy(self.GITLAB_API_TOKEN)
#        with self.assertRaises(HTTPError) as context:
#            pipeline_id = stable_deploy.find_latest_stable_version(project_id)
#        unauthorized_json = json.loads(str(context.exception))
#        self.assertTrue(unauthorized_json["status_code"], 404)

    #def test_stable_deploy_views_stable_deploy_ERROR(self):
    #    # error
    #    pipeline_id = "0000032"
    #    chat_id = "123456789"
    #    user = User()
    #    user.create_user("sudjoao")
    #    user.chat_id = chat_id
    #    project = Project()
    #    project.create_project(user, "abc", "ada_gitlab",
    #                           "https://gitlab.com/sudjoao/ada-gitlab/", [],
    #                           "12309295")
    #    user.project = project
    #    user.save()
    #    # Testar
    #    with (self.assertRaises(HTTPError )) as context:
    #        response = self.client.get("/stable_deploy/{chat_id}/".
    #        format(chat_id=chat_id))
    #    unauthorized_json = json.loads(str(context.exception))
    #    json_status_code = unauthorized_json["status_code"]
    #    if json_status_code == 404 or json_status_code == 401:
    #        assert True
    #    else:
    #        assert False

    #    User.delete(user)
