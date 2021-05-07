import json
import sys
import time
import unittest
import logging
from urllib.parse import quote

from flask import appcontext_pushed, g
from contextlib import contextmanager
from hive import create_app, HIVE_MODE_TEST
from tests.v2 import test_common

logger = logging.getLogger()
logger.level = logging.DEBUG


@contextmanager
def name_set(app, name):
    def handler(sender, **kwargs):
        g.app_name = name

    with appcontext_pushed.connected_to(handler, app):
        yield


class HiveMongoDbTestCase(unittest.TestCase):
    def __init__(self, methodName='runTest'):
        super(HiveMongoDbTestCase, self).__init__(methodName)

    @classmethod
    def setUpClass(cls):
        cls.stream_handler = logging.StreamHandler(sys.stdout)
        logger.addHandler(cls.stream_handler)
        logging.getLogger("HiveMongoDbTestCase").debug("Setting up HiveMongoDbTestCase\n")

    @classmethod
    def tearDownClass(cls):
        logging.getLogger("HiveMongoDbTestCase").debug("\n\nShutting down HiveMongoDbTestCase")
        logger.removeHandler(cls.stream_handler)

    def setUp(self):
        logging.getLogger("HiveMongoDbTestCase").info("\n")
        self.app = create_app(mode=HIVE_MODE_TEST)
        self.app.config['TESTING'] = True
        self.test_client = self.app.test_client()
        self.content_type = ("Content-Type", "application/json")

        self.json_header = [
            self.content_type,
        ]
        test_common.setup_test_auth_token()
        self.init_auth()
        self.clear_db()
        self.did = test_common.get_auth_did()
        self.app_id = test_common.get_auth_app_did()
        test_common.setup_test_vault(self.did)
        self.init_collection()
        self.init_col_item()

    def init_auth(self):
        token = test_common.get_auth_token()
        self.auth = [
            ("Authorization", "token " + token),
            self.content_type,
        ]

    def tearDown(self):
        test_common.delete_test_auth_token()
        logging.getLogger("HiveMongoDbTestCase").info("\n")

    def clear_db(self):
        logging.getLogger("HiveMongoDbTestCase").debug("\nRunning test_1_create_collection")
        r, s = self.parse_response(
            self.test_client.delete('/api/v2/vault/db/works',
                                    headers=self.auth)
        )
        self.assertEquals(s, 204)

    def parse_response(self, r):
        try:
            logging.getLogger("HiveMongoDbTestCase").debug("\nret:" + str(r.get_data()))
            v = json.loads(r.get_data())
        except json.JSONDecodeError:
            v = None
        return v, r.status_code

    def assert200(self, status):
        self.assertEqual(status, 200)

    def assert201(self, status):
        self.assertEqual(status, 201)

    def init_collection(self):
        logging.getLogger("HiveMongoDbTestCase").debug("\nRunning test_1_create_collection")
        r, s = self.parse_response(
            self.test_client.put('/api/v2/vault/db/works',
                                 headers=self.auth)
        )
        self.assert201(s)

        r, s = self.parse_response(
            self.test_client.put('/api/v2/vault/db/works',
                                 headers=self.auth)
        )
        self.assert200(s)

    def init_col_item(self):
        logging.getLogger("HiveMongoDbTestCase").debug("\nRunning test_1_insert")
        dic = {
            "document": [
                {
                    "author": "john doe1",
                    "title": "Eve for Dummies1_1"
                },
                {
                    "author": "john doe1",
                    "title": "Eve for Dummies1_2"
                },
                {
                    "author": "john doe1",
                    "title": "Eve for Dummies1_3"
                },
                {
                    "author": "john doe2",
                    "title": "Eve for Dummies2"
                },
                {
                    "author": "john doe3",
                    "title": "Eve for Dummies3"
                }
            ],
            "options": {"bypass_document_validation": False, "ordered": True}
        }
        self.insert_item("works", dic)

    def insert_item(self, col, doc):
        r, s = self.parse_response(
            self.test_client.post(f'/api/v2/vault/db/collection/{col}',
                                  data=json.dumps(doc),
                                  headers=self.auth)
        )
        self.assert201(s)

    def count_item(self, col, filter_dict, skip, limit):
        fi = quote(json.dumps(filter_dict))
        r, s = self.parse_response(
            self.test_client.get(f'/api/v2/vault/db/collection/{col}?count=true&filter={fi}&skip={skip}&limit={limit}',
                                 headers=self.auth)
        )
        self.assert200(s)
        return r['count']

    def get_item(self, col, filter_dict, skip, limit):
        fi = quote(json.dumps(filter_dict))
        r, s = self.parse_response(
            self.test_client.get(f'/api/v2/vault/db/collection/{col}?filter={fi}&skip={skip}&limit={limit}',
                                 headers=self.auth)
        )
        self.assert200(s)
        return r

    def test_count_documents(self):
        logging.getLogger("HiveMongoDbTestCase").debug("\nRunning test_count_documents")
        fi_dict = {"author": "john doe1"}
        count = self.count_item("works", fi_dict, 0, 10)
        self.assertEqual(3, count)

    def test_find(self):
        logging.getLogger("HiveMongoDbTestCase").debug("\nRunning test_find")
        fi_dict = {"author": "john doe1"}
        doc = self.get_item("works", fi_dict, 0, 2)
        items = doc["items"]
        for it in items:
            self.assertEqual(it["author"], "john doe1")

    def test_find_none_filter(self):
        logging.getLogger("HiveMongoDbTestCase").debug("\nRunning test_find_none_filter")
        fi_dict = {"author": "john doe1"}
        doc = self.get_item("works", fi_dict, 1, 2)
        items = doc["items"]
        self.assertEqual(2, len(items))

    def test_update_item(self):
        logging.getLogger("HiveMongoDbTestCase").debug("\nRunning test_update_item")
        r, s = self.parse_response(
            self.test_client.patch('/api/v2/vault/db/collection/works',
                                   data=json.dumps(
                                       {
                                           "filter": {
                                               "author": "john doe2",
                                           },
                                           "update": {"$set": {
                                               "author": "john doe2_2",
                                               "title": "Eve for Dummies2_2_1"
                                           }},
                                           "options": {
                                               "upsert": True,
                                               "bypass_document_validation": False
                                           }
                                       }
                                   ),
                                   headers=self.auth)
        )
        self.assert200(s)
        fi_dict = {"author": "john doe2"}
        count = self.count_item("works", fi_dict, 0, 10)
        self.assertEqual(0, count)

        fi_dict = {"author": "john doe2_2"}
        count = self.count_item("works", fi_dict, 0, 10)
        self.assertEqual(1, count)

    def test_delete_item(self):
        logging.getLogger("HiveMongoDbTestCase").debug("\nRunning test_delete_item")
        r, s = self.parse_response(
            self.test_client.delete('/api/v2/vault/db/collection/works',
                                    data=json.dumps(
                                        {
                                            "filter": {
                                                "author": "john doe3",
                                            }
                                        }
                                    ),
                                    headers=self.auth)
        )
        self.assertEqual(s, 204)
        fi_dict = {"author": "john doe3"}
        count = self.count_item("works", fi_dict, 0, 10)
        self.assertEqual(0, count)

    def test_delete_collection(self):
        logging.getLogger("HiveMongoDbTestCase").debug("\nRunning test_delete_collection")
        r, s = self.parse_response(
            self.test_client.delete('/api/v2/vault/db/works',
                                    headers=self.auth)
        )
        self.assertEqual(s, 204)

        r, s = self.parse_response(
            self.test_client.post('/api/v2/vault/db/collection/works',
                                  data=json.dumps(
                                      {
                                          "document": [
                                              {
                                                  "author": "john doe1",
                                                  "title": "Eve for Dummies1_2"
                                              },
                                              {
                                                  "author": "john doe2",
                                                  "title": "Eve for Dummies2"
                                              },
                                              {
                                                  "author": "john doe3",
                                                  "title": "Eve for Dummies3"
                                              }
                                          ],
                                          "options": {"bypass_document_validation": False, "ordered": True}
                                      }
                                  ),
                                  headers=self.auth)
        )
        self.assertEqual(s, 404)

        r, s = self.parse_response(
            self.test_client.patch('/api/v2/vault/db/collection/works',
                                   data=json.dumps(
                                       {
                                           "filter": {
                                               "author": "john doe3_1"
                                           },
                                           "update": {"$set": {
                                               "author": "john doe3_1",
                                               "title": "Eve for Dummies3_1"
                                           }},
                                           "options": {
                                               "upsert": True,
                                               "bypass_document_validation": False
                                           }
                                       }
                                   ),
                                   headers=self.auth)
        )
        self.assertEqual(s, 404)

        r, s = self.parse_response(
            self.test_client.delete('/api/v2/vault/db/collection/works',
                                    data=json.dumps(
                                        {
                                            "filter": {
                                                "author": "john doe3_1",
                                            }
                                        }
                                    ),
                                    headers=self.auth)
        )
        self.assertEqual(s, 404)


if __name__ == '__main__':
    unittest.main()
