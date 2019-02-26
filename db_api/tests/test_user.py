import unittest
import json
from main import app as tested_app
from models import db as tested_db
from config import TestConfig
from models import User

tested_app.config.from_object(TestConfig)


class TestUser(unittest.TestCase):
    def setUp(self):
        self.db = tested_db
        self.db.create_all()
        self.db.session.add(User(id=1, name="Alice", mail="alice@soen.com", pwdhash="steakhasher"))
        self.db.session.add(User(id=2, name="Bob", mail="bob@soen.com", pwdhash="steakhasher"))
        self.db.session.commit()

        self.app = tested_app.test_client()

    def tearDown(self):
        User.query.delete()
        self.db.session.commit()

    def test_get_all_User(self):
        response = self.app.get("/user/")
        self.assertEqual(response.status_code, 200)

        User_list = json.loads(str(response.data, "utf8"))
        self.assertEqual(type(User_list), list)
        self.assertDictEqual(User_list[0],
                             {"id": "1", "name": "Alice", "mail": "alice@soen.com"})
        self.assertDictEqual(User_list[1], {"id": "2", "name": "Bob", "mail": "bob@soen.com"})

    def test_get_User_with_valid_id(self):
        response = self.app.get("/user/1")
        self.assertEqual(response.status_code, 200)

        User = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(User, {"id": "1", "name": "Alice", "mail": "alice@soen.com"})

    def test_get_User_with_pwdhash(self):
        response = self.app.get("/user/info/alice@soen.com")
        self.assertEqual(response.status_code, 200)

        User = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(User, {"id": "1", "name": "Alice", "mail": "alice@soen.com", "pwdhash": "steakhasher"})

    def test_get_User_with_invalid_id(self):
        response = self.app.get("/user/1000000")
        self.assertEqual(response.status_code, 404)

        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 404, "msg": "User not found"})

    def test_post_User_without_id(self):
        response = self.app.post("/user/", data={"name": "Amy", "mail": "azd@azd.azd", "pwdhash": "yeet"})
        self.assertEqual(response.status_code, 200)

        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {'id': '3', "name": "Amy", "mail": "azd@azd.azd"})

    def test_post_User_without_name(self):
        initial_count = User.query.filter_by(name="Amy").count()

        response = self.app.post("/user/")
        self.assertEqual(response.status_code, 400)

        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 400, "msg": "missing parameters"})

        updated_count = User.query.filter_by(name="Amy").count()
        self.assertEqual(updated_count, initial_count)

    def test_post_User_with_new_id(self):
        response = self.app.post("/user/",
                                 data={"id": '3', "name": "Amy", "mail": "azd@azd.azd", "pwdhash": "steakhasher"})
        self.assertEqual(response.status_code, 200)

        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"id": '3', "name": "Amy", "mail": "azd@azd.azd"})

    def test_put_User(self):
        response = self.app.put("/user/1", data={"name": "Numericable"})
        self.assertEqual(response.status_code, 200)

        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"id": "1", "name": "Numericable", "mail": "alice@soen.com"})

    def test_put_User_with_wrong_id(self):
        response = self.app.put("/user/1984651")
        self.assertEqual(response.status_code, 404)

        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 404, "msg": "User not found"})

    def test_delete_User(self):
        initial_count = User.query.count()

        response = self.app.delete("/user/1")
        self.assertEqual(response.status_code, 200)

        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 200, "msg": "success"})

        updated_count = User.query.count()
        self.assertEqual(updated_count, initial_count - 1)

    def test_delete_wrong_User(self):
        initial_count = User.query.count()

        response = self.app.delete("/user/47962")
        self.assertEqual(response.status_code, 404)

        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 404, "msg": "User not found"})

        updated_count = User.query.count()
        self.assertEqual(updated_count, initial_count)
