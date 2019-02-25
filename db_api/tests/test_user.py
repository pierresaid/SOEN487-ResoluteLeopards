import unittest
import json
from main import app as tested_app
from models import db as tested_db
from config import TestConfig
from models import User

tested_app.config.from_object(TestConfig)


class TestUser(unittest.TestCase):
    def setUp(self):
        # set up the test DB
        self.db = tested_db
        self.db.create_all()
        self.db.session.add(User(id=1, name="Alice"))
        self.db.session.add(User(id=2, name="Bob"))
        self.db.session.commit()

        self.app = tested_app.test_client()

    def tearDown(self):
        # clean up the DB after the tests
        User.query.delete()
        self.db.session.commit()

    def test_get_all_User(self):
        # send the request and check the response status code
        response = self.app.get("/user/")
        self.assertEqual(response.status_code, 200)

        # convert the response data from json and call the asserts
        User_list = json.loads(str(response.data, "utf8"))
        self.assertEqual(type(User_list), list)
        self.assertDictEqual(User_list[0], {"id": "1", "name": "Alice"})
        self.assertDictEqual(User_list[1], {"id": "2", "name": "Bob"})

    def test_get_User_with_valid_id(self):
        # send the request and check the response status code
        response = self.app.get("/user/1")
        self.assertEqual(response.status_code, 200)

        # convert the response data from json and call the asserts
        User = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(User, {"id": "1", "name": "Alice"})

    def test_get_User_with_invalid_id(self):
        # send the request and check the response status code
        response = self.app.get("/user/1000000")
        self.assertEqual(response.status_code, 404)

        # convert the response data from json and call the asserts
        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 404, "msg": "Cannot find this user."})

    def test_post_User_without_id(self):
        # send the request and check the response status code
        response = self.app.post("/user/", data={"name": "Amy"})
        self.assertEqual(response.status_code, 200)

        # convert the response data from json and call the asserts
        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 200, "msg": "success"})

    def test_post_User_without_name(self):
        # do we really need to check counts?
        initial_count = User.query.filter_by(name="Amy").count()

        # send the request and check the response status code
        response = self.app.post("/user/")
        self.assertEqual(response.status_code, 400)

        # convert the response data from json and call the asserts
        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 400, "msg": "missing name"})

        # check if the DB was updated correctly
        updated_count = User.query.filter_by(name="Amy").count()
        self.assertEqual(updated_count, initial_count)

    def test_post_User_with_new_id(self):
        # send the request and check the response status code
        response = self.app.post("/user/", data={"id": 3, "name": "Amy"})
        self.assertEqual(response.status_code, 200)

        # convert the response data from json and call the asserts
        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 200, "msg": "success"})

        # check if the DB was updated correctly
        user = User.query.filter_by(id=3).first()
        self.assertEqual(user.name, "Amy")

    def test_put_User_without_name(self):
        # send the request and check the response status code
        response = self.app.put("/user/1")
        self.assertEqual(response.status_code, 400)

        # convert the response data from json and call the asserts
        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 400, "msg": "missing name"})

    def test_put_User_with_wrong_id(self):
        # send the request and check the response status code
        response = self.app.put("/user/1984651")
        self.assertEqual(response.status_code, 404)

        # convert the response data from json and call the asserts
        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 404, "msg": "Cannot find this user."})

    def test_delete_User(self):
        initial_count = User.query.count()

        # send the request and check the response status code
        response = self.app.delete("/user/1")
        self.assertEqual(response.status_code, 200)

        # convert the response data from json and call the asserts
        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 200, "msg": "success"})

        # check if the DB was updated correctly
        updated_count = User.query.count()
        self.assertEqual(updated_count, initial_count - 1)

    def test_delete_wrong_User(self):
        initial_count = User.query.count()

        # send the request and check the response status code
        response = self.app.delete("/user/47962")
        self.assertEqual(response.status_code, 404)

        # convert the response data from json and call the asserts
        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 404, "msg": "Cannot find this user."})

        # check if the DB was updated correctly
        updated_count = User.query.count()
        self.assertEqual(updated_count, initial_count)
