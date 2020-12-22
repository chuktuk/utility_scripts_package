#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-


"""Unit tests for the fsconn module."""

import os
import unittest
from utility_scripts import fsconn


class TestInitFSConn(unittest.TestCase):
    def setUp(self):
        os.environ['SSH_KEYPATH'] = 'path'
        os.environ['SSH_HOST'] = 'host'
        os.environ['SSH_USERNAME'] = 'username'

        os.environ['SSH_DEV_KEYPATH'] = 'dev/path'
        os.environ['SSH_DEV_HOST'] = 'dev.host'
        os.environ['SSH_DEV_USERNAME'] = 'dev_username'

    def test_init_env_vars_dev(self):
        conn = fsconn.FSConnection(env='development')
        self.assertEqual('dev/path', conn._FSConnection__keyfilepath)
        self.assertEqual('dev.host', conn._FSConnection__host)
        self.assertEqual('dev_username', conn._FSConnection__username)
        self.assertEqual('Protected data.', conn.keyfilepath)
        self.assertEqual('Protected data.', conn.host)
        self.assertEqual('Protected data.', conn.username)
        self.assertEqual(22, conn.port)

    def test_init_env_vars_prod(self):
        conn = fsconn.FSConnection(env='production')
        self.assertEqual('path', conn._FSConnection__keyfilepath)
        self.assertEqual('host', conn._FSConnection__host)
        self.assertEqual('username', conn._FSConnection__username)
        self.assertEqual('Protected data.', conn.keyfilepath)
        self.assertEqual('Protected data.', conn.host)
        self.assertEqual('Protected data.', conn.username)
        self.assertEqual(22, conn.port)


class TestKeyFilePath(unittest.TestCase):
    def setUp(self):
        self.conn = fsconn.FSConnection()
        files = [i for i in os.listdir() if os.path.isfile(i)]
        if files:
            self.file = files[0]
        else:
            raise FileNotFoundError('Unable to test TestKeyFilePath: no files in current working directory.')
        self.valid_path_invalid_file = ''.join([os.getcwd().replace('\\', '/'), '/good-luck-finding-me.lmnop'])
        self.invalid_path = 'path/that/doesnt/exist/anywhere/'

    def test_valid_path(self):
        if self.file:
            self.conn.keyfilepath = self.file
        else:
            raise FileNotFoundError('Unable to test TestKeyFilePath.test_valid_path: no files in current working '
                                    'directory.')

    def test_valid_path_invalid_file(self):
        try:
            self.conn.keyfilepath = self.valid_path_invalid_file
            raise Exception
        except Exception as e:
            self.assertIsInstance(e, FileNotFoundError)

    def test_invalid_path(self):
        try:
            self.conn.keyfilepath = self.invalid_path
            raise Exception
        except Exception as e:
            self.assertIsInstance(e, FileNotFoundError)


class InvalidDataTypes(unittest.TestCase):
    def setUp(self):
        self.conn = fsconn.FSConnection()

    def test_keyfilepath(self):
        for item in [4, {}, []]:
            try:
                self.conn.keyfilepath = item
                raise Exception
            except Exception as e:
                self.assertIsInstance(e, TypeError)

    def test_host(self):
        for item in [4, {}, []]:
            try:
                self.conn.keyfilepath = item
                raise Exception
            except Exception as e:
                self.assertIsInstance(e, TypeError)

    def test_username(self):
        for item in [4, {}, []]:
            try:
                self.conn.username = item
                raise Exception
            except Exception as e:
                self.assertIsInstance(e, TypeError)

    def test_port(self):
        for item in ['nope', {}, []]:
            try:
                self.conn.port = item
                raise Exception
            except Exception as e:
                self.assertIsInstance(e, TypeError)


if __name__ == '__main__':
    unittest.main()
