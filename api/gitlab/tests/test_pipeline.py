import json
import unittest

from gitlab.tests.base import BaseTestCase


class TestPing(BaseTestCase):

    def test_ping(self):
        response = self.client.get('/pipeline/ping')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('pong!', data['message'])
        self.assertIn('success', data['status'])


if __name__ == '__main__':
    unittest.main()
