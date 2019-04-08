import unittest
import json
from main import app as tested_app
from config import TestConfig

tested_app.config.from_object(TestConfig)


class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = tested_app.test_client()

    def test_404_on_invalid_url(self):
        # send the request and check the response status code
        response = self.app.get("/something")
        self.assertEqual(response.status_code, 404)

        # convert the response data from json and call the asserts
        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 404, "msg": "404: Not Found"})

    def test_root(self):
        # send the request and check the response status code
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)

        # convert the response data from json and call the asserts
        body = json.loads(str(response.data, "utf8"))
#        self.assertEqual(body["title"], "SOEN487 project")
#        self.assertEqual(body["team"], "ResoluteLeopards")
