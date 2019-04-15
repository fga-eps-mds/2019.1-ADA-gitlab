# api/gitlab/tests/base.py


from flask_testing import TestCase

from gitlab import create_app


class BaseTestCase(TestCase):
    def create_app(self):
        app = create_app()
        app.config.from_object("gitlab.config.TestingConfig")
        return app
