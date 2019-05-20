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


class TestStableDeploy(BaseTestCase):
    GITLAB_API_TOKEN = os.getenv("GITLAB_API_TOKEN", "")

    def setup(self):
        init_db()
        Project.drop_collection()
        User.drop_collection()

    def test_stable_deploy_utils_run_stable_deploy(self):
        pass

    def test_stable_deploy_utils_find_latest_stable_version(self):
        pass

    def test_stable_deploy_views_ping_pong(self):
        pass

    def test_stable_deploy_views_stable_deploy(self):
        pass
