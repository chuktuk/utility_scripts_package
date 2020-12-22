#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-


import os
import logging
from datetime import datetime as dt
import unittest

from utility_scripts import log


class TestCreateFileLogger(unittest.TestCase):
    def setUp(self):
        if not os.path.exists('./log/'):
            os.mkdir('./log/')
            self.remove_dir = True
        else:
            self.remove_dir = False
        self.filename = ''.join(['./log/', dt.now().strftime('%Y%m%d_%H%M%S%f'), '_test_log.log'])
        self.logger = log.create_file_logger(self.filename, __name__, level='DEBUG')
        self.logger.info('Setup Complete.')

    def test_writing_log(self):
        with self.assertLogs(logger=self.logger, level='DEBUG') as cm:
            self.logger.debug('First test message, level debug.')
            self.logger.info('Second test message, level info.')
            self.logger.warning('Third test message, level warning.')
            self.logger.error('Fourth test message, level error.')
            self.logger.critical('Fifth test message, level critical.')
            self.assertEqual(len(cm.records), 5)

    def test_reading_log(self):
        with open(self.filename, 'r') as file:
            contents = file.read()
        self.assertIn('- test_log - INFO - Setup Complete.', contents)

    def tearDown(self):
        self.logger.info('Tearing down log.')
        fh = self.logger.handlers[0]
        self.logger.removeHandler(fh)
        logging.shutdown()
        os.remove(self.filename)
        if self.remove_dir:
            os.removedirs('./log/')


class TestProcessLogForErrors(unittest.TestCase):
    def setUp(self):
        if not os.path.exists('./log/'):
            os.mkdir('./log/')
            self.remove_dir = True
        else:
            self.remove_dir = False
        self.filename = ''.join(['./log/', dt.now().strftime('%Y%m%d_%H%M%S%f'), '_test_log.log'])
        self.logger = log.create_file_logger(self.filename, __name__, level='DEBUG')
        self.logger.info('Setup Complete.')

    def test_log_for_errors1(self):
        check, highest_level = log.process_log_for_errors(self.filename, level='WARNING')
        self.assertFalse(check)
        self.assertEqual(highest_level, 'INFO')

    def test_log_for_errors2(self):
        check, highest_level = log.process_log_for_errors(self.filename, level='DEBUG')
        self.assertTrue(check)
        self.assertEqual(highest_level, 'INFO')

    def test_log_for_errors3(self):
        self.logger.error('This is an error.')
        check, highest_level = log.process_log_for_errors(self.filename, level='ERROR')
        self.assertTrue(check)
        self.assertEqual(highest_level, 'ERROR')

    def test_log_for_errors4(self):
        self.logger.warning('This is a warning.')
        check, highest_level = log.process_log_for_errors(self.filename, level='ERROR')
        self.assertFalse(check)
        self.assertEqual(highest_level, 'WARNING')

    def test_log_for_errors5(self):
        self.logger.critical('This is a critical error.')
        check, highest_level = log.process_log_for_errors(self.filename, level='ERROR')
        self.assertTrue(check)
        self.assertEqual(highest_level, 'CRITICAL')

    def tearDown(self):
        self.logger.info('Tearing down log.')
        fh = self.logger.handlers[0]
        self.logger.removeHandler(fh)
        logging.shutdown()
        os.remove(self.filename)
        if self.remove_dir:
            os.removedirs('./log/')


class TestShutdownLogging(unittest.TestCase):
    def setUp(self):
        if not os.path.exists('./log/'):
            os.mkdir('./log/')
            self.remove_dir = True
        else:
            self.remove_dir = False
        self.filename = ''.join(['./log/', dt.now().strftime('%Y%m%d_%H%M%S%f'), '_test_log.log'])
        self.logger = log.create_file_logger(self.filename, __name__, level='DEBUG')
        self.logger.info('Setup Complete.')

    def test_shutdown_logging(self):
        log.shutdown_logging(self.logger)

        self.logger.info('Nope, still logging.')

        with open(self.filename, 'r') as file:
            contents = file.read()
        self.assertNotIn('- test_log - INFO - Nope, still logging.', contents)

    def tearDown(self):
        try:
            # ensure logging is shutdown if the test failed
            fh = self.logger.handlers[0]
            self.logger.removeHandler(fh)
            logging.shutdown()
        except:
            pass
        os.remove(self.filename)
        if self.remove_dir:
            os.removedirs('./log/')


if __name__ == '__main__':
    unittest.main()
