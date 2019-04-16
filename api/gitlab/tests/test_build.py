import json
from gitlab.tests.base import BaseTestCase


class Testbuild(BaseTestCase):
    def test_ping_pong(self):
        response = self.client.get("/build/ping")
        json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
