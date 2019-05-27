# api/gitlab/tests/base.py


from flask_testing import TestCase
from gitlab.data import init_db
from gitlab import create_app


class BaseTestCase(TestCase):
    def setUp(self):
        self.db = init_db()

    def create_app(self):
        app = create_app()
        app.config.from_object("gitlab.config.TestingConfig")
        return app

    def tearDown(self):
        self.db.drop_database('api')
