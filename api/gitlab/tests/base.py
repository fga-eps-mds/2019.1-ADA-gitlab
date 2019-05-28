# api/gitlab/tests/base.py


from flask_testing import TestCase
from gitlab.data import init_db
from gitlab import create_app
from gitlab.data.user import User
from gitlab.data.project import Project
import os


class BaseTestCase(TestCase):
    def setUp(self):
        self.db = init_db()
        self.user = User()
        self.user.username = 'joaovitor'
        self.user.chat_id = '123456789'
        self.user.gitlab_user = 'joaovitor3'
        self.user.gitlab_user_id = '1195203'
        self.user.access_token = os.getenv("GITLAB_API_TOKEN", "")
        self.user.save()
        self.project = Project()
        self.project_name = 'ada-gitlab'
        self.project_id = '11789629'
        self.project.save_webhook_infos(self.user, self.project_name,
                                        self.project_id)
        self.user.save_gitlab_repo_data(self.project)
        self.GITLAB_API_TOKEN = os.getenv("GITLAB_API_TOKEN", "")

    def create_app(self):
        app = create_app()
        app.config.from_object("gitlab.config.TestingConfig")
        return app

    def tearDown(self):
        self.db.drop_database('api')
