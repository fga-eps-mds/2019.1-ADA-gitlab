# api/gitlab/tests/base.py


from flask_testing import TestCase
from gitlab.data import init_db
from gitlab import create_app
from gitlab.data.user import User
from gitlab.data.project import Project
from requests import Response


class BaseTestCase(TestCase):
    def setUp(self):
        self.db = init_db()
        self.user = User()
        self.user.username = 'ada'
        self.user.chat_id = '339847919'
        self.user.gitlab_user = 'adatestbot'
        self.user.gitlab_user_id = '4047441'
        self.user.access_token = "123456"
        self.user.save()
        self.project = Project()
        self.project_name = 'ada-gitlab'
        self.project_id = '12532279'
        self.project.save_webhook_infos(self.user, self.project_name,
                                        self.project_id)
        self.user.save_gitlab_repo_data(self.project)
        self.GITLAB_API_TOKEN = "12345"

        self.mocked_404_response = Response()
        self.mocked_404_response.status_code = 404

    def create_app(self):
        app = create_app()
        app.config.from_object("gitlab.config.TestingConfig")
        return app

    def tearDown(self):
        self.db.drop_database('api')
