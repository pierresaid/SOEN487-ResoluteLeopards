import unittest
import json
from main import app as tested_app
from models import db as tested_db
from config import TestConfig
from models import Post

tested_app.config.from_object(TestConfig)


class TestPost(unittest.TestCase):
    def setUp(self):

        # set up the test DB
        self.db = tested_db
        self.db.create_all()
        self.db.session.add(Post(id=1, title="Hello"))
        self.db.session.add(Post(id=2, title="World"))
        self.db.session.commit()

        self.app = tested_app.test_client()

    def tearDown(self):
        # clean up the DB after the tests
        Post.query.delete()
        self.db.session.commit()

    def test_get_all_Post(self):
        # send the request and check the response status code
        response = self.app.get("/post/")
        self.assertEqual(response.status_code, 200)

        # convert the response data from json and call the asserts
        Post_list = json.loads(str(response.data, "utf8"))
        self.assertEqual(type(Post_list), list)
        self.assertDictEqual(Post_list[0], {"id": "1", "title": "Hello"})
        self.assertDictEqual(Post_list[1], {"id": "2", "title": "World"})

    def test_get_Post_with_valid_id(self):
        # send the request and check the response status code
        response = self.app.get("/post/1")
        self.assertEqual(response.status_code, 200)

        # convert the response data from json and call the asserts
        Post = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(Post, {"id": "1", "title": "Hello"})

    def test_get_Post_with_invalid_id(self):
        # send the request and check the response status code
        response = self.app.get("/post/1000000")
        self.assertEqual(response.status_code, 404)

        # convert the response data from json and call the asserts
        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 404, "msg": "Cannot find this post."})

    def test_post_Post_without_id(self):
        # do we really need to check counts?
        initial_count = Post.query.filter_by(title="Wow").count()

        # send the request and check the response status code
        response = self.app.post("/post/", data={"title": "Wow"})
        self.assertEqual(response.status_code, 200)

        # convert the response data from json and call the asserts
        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 200, "msg": "success"})

        # check if the DB was updated correctly
        updated_count = Post.query.filter_by(title="Wow").count()
        self.assertEqual(updated_count, initial_count + 1)

    def test_post_Post_without_title(self):
        # send the request and check the response status code
        response = self.app.post("/post/")
        self.assertEqual(response.status_code, 400)

        # convert the response data from json and call the asserts
        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 400, "msg": "missing title"})

    def test_post_Post_with_new_id(self):
        # send the request and check the response status code
        response = self.app.post("/post/", data={"id": 3, "title": "Wow"})
        self.assertEqual(response.status_code, 200)

        # convert the response data from json and call the asserts
        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 200, "msg": "success"})

        # check if the DB was updated correctly
        post = Post.query.filter_by(id=3).first()
        self.assertEqual(post.title, "Wow")

    def test_put_Post_without_title(self):
        # send the request and check the response status code
        response = self.app.put("/post/1")
        self.assertEqual(response.status_code, 400)

        # convert the response data from json and call the asserts
        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 400, "msg": "missing title"})

    def test_put_Post_with_wrong_id(self):
        # send the request and check the response status code
        response = self.app.put("/post/1984651")
        self.assertEqual(response.status_code, 404)

        # convert the response data from json and call the asserts
        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 404, "msg": "Cannot find this post."})

    def test_delete_Post(self):
        initial_count = Post.query.count()

        # send the request and check the response status code
        response = self.app.delete("/post/1")
        self.assertEqual(response.status_code, 200)

        # convert the response data from json and call the asserts
        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 200, "msg": "success"})

        # check if the DB was updated correctly
        updated_count = Post.query.count()
        self.assertEqual(updated_count, initial_count - 1)

    def test_delete_wrong_Post(self):
        initial_count = Post.query.count()

        # send the request and check the response status code
        response = self.app.delete("/post/47962")
        self.assertEqual(response.status_code, 404)

        # convert the response data from json and call the asserts
        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 404, "msg": "Cannot find this post."})

        # check if the DB was updated correctly
        updated_count = Post.query.count()
        self.assertEqual(updated_count, initial_count)
