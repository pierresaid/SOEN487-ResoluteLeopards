import unittest
from main import app as test_app
from config import TestConfig


class TestUser(unittest.TestCase):
    def setUp(self):
        test_app.testing = True
        self.app = test_app.test_client()

    def test_users_get(self):
        response = self.app.get("/users/")

        # HTTP is correct
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers.get("Content-Type"), "application/json")

        json = response.get_json()
        print('RESPONSE: ', json)
        pass

