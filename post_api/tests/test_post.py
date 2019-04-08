import unittest
import json
from main import app as tested_app
from main import db as tested_db
from config import TestConfig
from post_models import Post

tested_app.config.from_object(TestConfig)


class TestPost(unittest.TestCase):
    def setUp(self):
        # set up the tests DB
        self.db = tested_db
        self.db.create_all()
        self.db.session.add(Post(title="Hello", url_one="url1", url_two="url2", author_id=1))
        self.db.session.add(Post(title="World", url_one="url1", url_two="url2", author_id=1))
        self.db.session.commit()

        self.app = tested_app.test_client()

    def tearDown(self):
        # clean up the DB after the tests
        Post.query.delete()
        self.db.session.commit()

    def test_get_all_Post(self):
        # send the request and check the response status code
        response = self.app.get("/post")
        self.assertEqual(response.status_code, 200)

        # convert the response data from json and call the asserts
        Post_list = json.loads(str(response.data, "utf8"))
        self.assertEqual(type(Post_list), dict)
        assert set({"id": "1", "title": "Hello", "url_one": "url1", "url_two": "url2", "author_id": '1'}.items())\
            .issubset(set(Post_list['posts'][0].items()))
        assert set({"id": "2", "title": "World", "url_one": "url1", "url_two": "url2", "author_id": '1'}.items())\
            .issubset(set(Post_list['posts'][1].items()))
        
    def test_get_Post_with_valid_id(self):
        # send the request and check the response status code
        response = self.app.get("/post/1")
        self.assertEqual(response.status_code, 200)

        # convert the response data from json and call the asserts
        post = json.loads(str(response.data, "utf8"))['post']
        self.assertDictEqual(post, {"id": "1", "title": "Hello", "url_one": "url1", "url_two": "url2", 'author_id': '1'})

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
        response = self.app.post("/post", data={"title": "Wow", "url_one": "url1", "url_two": "url2", 'user_id': '1'})
        self.assertEqual(response.status_code, 200)

        # convert the response data from json and call the asserts
        body = json.loads(str(response.data, "utf8"))['post']
        self.assertDictEqual(body, {"id" : "3", "title": "Wow", "url_one": "url1", "url_two": "url2", 'author_id': '1'})

        # check if the DB was updated correctly
        updated_count = Post.query.filter_by(title="Wow").count()
        self.assertEqual(updated_count, initial_count + 1)

    def test_post_Post_without_title(self):
        # send the request and check the response status code
        response = self.app.post("/post")
        self.assertEqual(response.status_code, 400)

        # convert the response data from json and call the asserts
        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 400, "msg": "Badly formed request, parameters are missing"})

    def test_post_Post_with_new_id(self):
        # send the request and check the response status code
        response = self.app.post("/post", data={"title": "Wow", "url_one": "url1", "url_two": "url2", "user_id": "1"})
        self.assertEqual(response.status_code, 200)

        # convert the response data from json and call the asserts
        body = json.loads(str(response.data, "utf8"))['post']
        self.assertDictEqual(body, {"id": "3", "title": "Wow", "url_one": "url1", "url_two": "url2", "author_id": "1"})

        # check if the DB was updated correctly
        post = Post.query.filter_by(id=3).first()
        self.assertEqual(post.title, "Wow")

    def test_post_Post(self):
        # send the request and check the response status code
        response = self.app.post("/post", data={"title": "new titre", "url_one": "url1", "url_two": "url2", "user_id": "1"})
        self.assertEqual(response.status_code, 200)

        response = self.app.get("/post/3")
        self.assertEqual(response.status_code, 200)

        # convert the response data from json and call the asserts
        post = json.loads(str(response.data, "utf8"))['post']
        self.assertDictEqual(post, {"id": "3", "title": "new titre", "url_one": "url1", "url_two": "url2", "author_id": "1"})

    def test_get_Post_with_wrong_id(self):
        # send the request and check the response status code
        response = self.app.get("/post/1984651")
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
