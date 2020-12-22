#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-

import unittest

from utility_scripts import dbase
from tests.conftest import initialize_unittest_db

from pymongo import results


class TestGetMongoClient(unittest.TestCase):
    def test_missing_uri(self):
        self.assertRaises(ValueError, dbase.get_mongo_client, timeout=300000)


class TestPyMongo(unittest.TestCase):
    def setUp(self):
        self.col = initialize_unittest_db(add_records=False)
        self.result_one = self.col.insert_one({'name': 'test', 'value': 12345})
        self.result_many = self.col.insert_many([{'name': 'test2', 'value': 9876}, {'name': 'test3', 'value': 42}])
        self.docs = self.col.find({}, {'_id': False})
        self.docs = [doc for doc in self.docs]

    def test_pymongo_inserts(self):
        # test insert operations
        self.assertIsInstance(self.result_one, results.InsertOneResult)
        self.assertIsInstance(self.result_many, results.InsertManyResult)

    def test_find_operations(self):
        self.assertEqual(len(self.docs), 3)

    def test_doc_values(self):
        self.assertCountEqual(self.docs, [{'name': 'test', 'value': 12345},
                                          {'name': 'test2', 'value': 9876},
                                          {'name': 'test3', 'value': 42}])


class TestInsertIntoMongo(unittest.TestCase):
    def setUp(self):
        self.col = initialize_unittest_db(add_records=False)
        self.one_record = {'name': 'test', 'key2': 'value', 'value': 'this is my value'}

        self.multiple_records = [{'name': 'test2', 'key2': 'another value', 'value': 9876},
                                 {'name': 'test3', 'key2': 'yet another value', 'value': 42}]

        # adds the records to mongo
        self.result_one = dbase.insert_into_mongo(self.one_record, self.col)
        self.result_many = dbase.insert_into_mongo(self.multiple_records, self.col)

    def test_insert_one_into_mongo(self):
        self.assertIsInstance(self.result_one, results.InsertOneResult)

    def test_insert_many_into_mongo(self):
        self.assertIsInstance(self.result_many, results.InsertManyResult)

    def test_insert_results(self):
        docs = self.col.find({}, {'_id': False})
        docs = [doc for doc in docs]
        self.assertEqual(len(docs), 3)
        self.assertCountEqual(docs, [{'name': 'test', 'key2': 'value', 'value': 'this is my value'},
                                     {'name': 'test2', 'key2': 'another value', 'value': 9876},
                                     {'name': 'test3', 'key2': 'yet another value', 'value': 42}])


class TestUpsertIntoMongo(unittest.TestCase):
    def setUp(self):
        self.col = initialize_unittest_db(add_records=True)

    def test_upsert_into_mongo(self):
        # upserting using one field to identify unique records
        new_data = [{'name': 'test4', 'key2': 'value', 'value': 'I should be added'},
                    {'name': 'test', 'key2': 'I should be updated', 'value': 'I should be updated'}]

        deleted_records, delete_result, insert_result = dbase.upsert_into_mongo(new_data, unique_id='name',
                                                                                collection=self.col)

        for doc in deleted_records:
            doc.pop('_id')

        self.assertCountEqual(deleted_records, [{'name': 'test', 'key2': 'value', 'value': 'this is my value'}])

        docs = self.col.find({}, {'_id': False})
        docs = [doc for doc in docs]
        self.assertEqual(len(docs), 4)
        self.assertCountEqual(docs, [{'name': 'test', 'key2': 'I should be updated', 'value': 'I should be updated'},
                                     {'name': 'test2', 'key2': 'another value', 'value': 9876},
                                     {'name': 'test3', 'key2': 'yet another value', 'value': 42},
                                     {'name': 'test4', 'key2': 'value', 'value': 'I should be added'}])

    def test_upset_into_mongo_two(self):
        # upsert using two fields to identify unique records
        new_data = [{'name': 'test', 'key2': 'I should be added', 'value': 12345},
                    {'name': 'test2', 'key2': 'another value', 'value': 'I should be updated'},
                    {'name': 'test3', 'key2': 'yet another value', 'value': 'I should also be updated'}]

        # update two of the records and add a new record
        deleted_records, delete_result, insert_result = dbase.upsert_into_mongo(new_data,
                                                                                unique_id=['name', 'key2'],
                                                                                collection=self.col)

        self.assertEqual(len(deleted_records), 2)

        for doc in deleted_records:
            doc.pop('_id')

        self.assertCountEqual(deleted_records, [{'name': 'test2', 'key2': 'another value', 'value': 9876},
                                                {'name': 'test3', 'key2': 'yet another value', 'value': 42}])

        # verify the data in the collection
        docs = self.col.find({}, {'_id': False})
        docs = [doc for doc in docs]
        self.assertEqual(len(docs), 4)
        self.assertCountEqual(docs, [{'name': 'test', 'key2': 'value', 'value': 'this is my value'},
                                     {'name': 'test', 'key2': 'I should be added', 'value': 12345},
                                     {'name': 'test2', 'key2': 'another value', 'value': 'I should be updated'},
                                     {'name': 'test3', 'key2': 'yet another value',
                                      'value': 'I should also be updated'}])


if __name__ == '__main__':
    unittest.main()
