import unittest
from flask import current_app
from flask_testing import TestCase
from gitlab import create_app


class TestDevelopmentConfig(TestCase):
    def create_app(self):
        app = create_app()
        app.config.from_object("gitlab.config.DevelopmentConfig")
        return app

    def test_app_is_development(self):
        self.assertFalse(current_app is None)


if __name__ == "__main__":
    unittest.main()
