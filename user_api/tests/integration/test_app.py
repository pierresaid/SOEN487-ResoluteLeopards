import unittest
from json import loads as json_loads
from main import app as test_app
from keys import load_keys
from config import TestConfig
from jwcrypto import jwt, jws, jwk

test_app.config.from_object(TestConfig)


class TestApp(unittest.TestCase):
    def setUp(self):
        test_app.testing = True
        self.app = test_app.test_client()
        load_keys(test_app.config["KEY_LIST_PATH"])
        with open("../keys/test_key.pem", mode="rb") as key_file:
            self.key = jwk.JWK.from_pem(key_file.read())
            key_file.close()

    def test_404_on_invalid_url(self):
        # send the request and check the response status code
        response = self.app.get("/something")
        self.assertEqual(response.status_code, 404)

    def test_public_keys(self):
        response = self.app.get("/jwt/key")
        print(response.get_json())

        # HTTP is correct
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers.get("Content-Type"), "application/json")

        # Content
        json = response.get_json()
        self.assertTrue("keys" in json)
        self.assertTrue(isinstance(json["keys"], list))
        self.assertEqual(len(json["keys"]), 1)

        # Check the key is indeed the test key
        self.assertTrue("kid" in json["keys"][0])
        self.assertEqual(json["keys"][0]["kid"], "test_key")

    def test_obtain_token(self):
        response = self.app.get("/jwt/obtain")

        # HTTP is correct
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers.get("Content-Type"), "application/json")

        # Content
        json = response.get_json()
        self.assertTrue("token" in json)
        try:
            tok: jws.JWS = jwt.JWT(jwt=json["token"]).token
            tok.verify(self.key)
        except:
            self.fail("Obtained token could not be verified")
