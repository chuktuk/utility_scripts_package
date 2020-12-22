#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-


"""conftest.py unittest configuration.

To run unit tests, run the following from the /utility_scripts_package directory:

(or just python for windows)
python3 -m unittest discover -v tests
"""


from pymongo import MongoClient


# ensure pymongo unittest db/col initialized
def initialize_unittest_db(add_records=True):
    """Creates a session db for testing."""
    client = MongoClient(maxIdleTimeMS=300000)
    db = client['unittest']
    col = db['unittest']

    col.delete_many({})

    if add_records:
        col.insert_many([{'name': 'test', 'key2': 'value', 'value': 'this is my value'},
                         {'name': 'test2', 'key2': 'another value', 'value': 9876},
                         {'name': 'test3', 'key2': 'yet another value', 'value': 42}])

    return col
