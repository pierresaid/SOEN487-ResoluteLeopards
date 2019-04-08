import unittest
import json
from main import app as tested_app, db as tested_db
from post_models import Post,Vote
from config import TestConfig

tested_app.config.from_object(TestConfig)


class TestVote(unittest.TestCase):
    def setUp(self):
        # set up the tests DB
        self.db = tested_db
        self.db.create_all()
        self.db.session.add(Post(title="Hello", url_one="url1", url_two="url2", author_id='1'))
        self.db.session.add(Post(title="World", url_one="url1", url_two="url2", author_id='1'))
        self.db.session.commit()
        self.db.session.add(Vote(user_id=1, post_id=1, value=0))
        self.db.session.add(Vote(user_id=1, post_id=2, value=0))
        self.db.session.commit()

        self.app = tested_app.test_client()

    def tearDown(self):
        # clean up the DB after the tests
        Vote.query.delete()
        Post.query.delete()
        self.db.session.commit()

    def test_get_all_Vote(self):
        # send the request and check the response status code
        response = self.app.get("/vote")
        self.assertEqual(response.status_code, 200)

        # convert the response data from json and call the asserts
        Vote_list = json.loads(str(response.data, "utf8"))
        self.assertEqual(type(Vote_list), list)
        self.assertDictEqual(Vote_list[0], {"id": "1", "user_id": "1", "post_id": "1", "value": "0"})
        self.assertDictEqual(Vote_list[1], {"id": "2", "user_id": "1", "post_id": "2", "value": "0"})

    def test_get_Vote_with_valid_id(self):
        # send the request and check the response status code
        response = self.app.get("/vote/1/1")
        self.assertEqual(response.status_code, 200)

        # convert the response data from json and call the asserts
        Vote = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(Vote, {"id": "1", "user_id": "1", "post_id": "1", "value": "0"})

    def test_get_Vote_with_invalid_id(self):
        # send the request and check the response status code
        response = self.app.get("/vote/234/234")
        self.assertEqual(response.status_code, 404)

        # convert the response data from json and call the asserts
        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 404, "msg": "Cannot find this vote."})

    def test_post_Vote_with_no_data(self):
        # send the request and check the response status code
        response = self.app.post("/vote/")
        self.assertEqual(response.status_code, 400)

        # convert the response data from json and call the asserts
        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 400, "msg": "Request is missing fields"})

    def test_post_Vote_with_new_id(self):
        # send the request and check the response status code
        response = self.app.post("/vote/", data={"user_id": "2", "post_id": "2", "value": "0", "author_id": "1"})
        self.assertEqual(response.status_code, 200)

        # convert the response data from json and call the asserts
        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"id": "3", "user_id": "2", "post_id": "2", "value": "0"})

        # check if the DB was updated correctly
        vote = Vote.query.filter_by(user_id=2, post_id=2).first()
        self.assertEqual(vote.user_id, 2)
        self.assertEqual(vote.post_id, 2)
        self.assertEqual(vote.value, 0)

    def test_get_Vote_with_wrong_id(self):
        # send the request and check the response status code
        response = self.app.get("/vote/1984651/123")
        self.assertEqual(response.status_code, 404)

        # convert the response data from json and call the asserts
        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 404, "msg": "Cannot find this vote."})

    def test_change_Vote(self):
        response = self.app.put("/vote/1/1", data={"value" : "1"})
        self.assertEqual(response.status_code, 200)

        # send the request and check the response status code
        response = self.app.get("/vote/1/1")
        self.assertEqual(response.status_code, 200)

        # convert the response data from json and call the asserts
        Vote = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(Vote, {"id": "1", "user_id": "1", "post_id": "1", "value": "1"})

    def test_delete_Vote(self):
        initial_count = Vote.query.count()

        # send the request and check the response status code
        response = self.app.delete("/vote/1/1")
        self.assertEqual(response.status_code, 200)

        # convert the response data from json and call the asserts
        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 200, "msg": "success"})

        # check if the DB was updated correctly
        updated_count = Vote.query.count()
        self.assertEqual(updated_count, initial_count - 1)

    def test_delete_wrong_Vote(self):
        initial_count = Vote.query.count()

        # send the request and check the response status code
        response = self.app.delete("/vote/47962/123")
        self.assertEqual(response.status_code, 404)

        # convert the response data from json and call the asserts
        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 404, "msg": "Cannot find this vote."})

        # check if the DB was updated correctly
        updated_count = Vote.query.count()
        self.assertEqual(updated_count, initial_count)
