#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-


from utility_scripts import email

import os
import unittest


class TestEmailValidationFxn(unittest.TestCase):
    def setUp(self):
        self.addrs_pass = ['test@test.com', 'test@test.org', 'test@test.gov', 'test@test.au']
        self.addrs_fail = ['nope.com', 'uhuh@me', 'notgonna@.pass', '@cant.wont', 'back.wards@com']

    def test_email_valid(self):
        results = all([email.validate_email(addr) for addr in self.addrs_pass])
        self.assertTrue(results)

    def test_email_fail(self):
        results = all([not email.validate_email(addr) for addr in self.addrs_fail])
        self.assertTrue(results)


class TestInitMailEnvVars(unittest.TestCase):
    def setUp(self):
        os.environ['MAIL_SENDER'] = 'test@test.com'
        os.environ['MAIL_RECIPIENT'] = 'test@test.com'
        os.environ['MAIL_BODY'] = 'This is the email body.'
        # testing init with default mail port
        os.environ['MAIL_PASSWORD'] = 'supersecret'
        os.environ['MAIL_SUBJECT'] = 'This is the subject.'
        os.environ['MAIL_SERVER'] = 'smtp.thisdoesntexist.com'
        os.environ['MAIL_USERNAME'] = 'myusername'
        # using default tls setting of False

        self.mail = email.Mail()

    def test_getenv_during_init(self):
        self.assertEqual(self.mail.sender, 'test@test.com')
        self.assertEqual(self.mail.recipient, 'test@test.com')
        self.assertEqual(self.mail.body, 'This is the email body.')
        self.assertEqual(self.mail.password, 'Value is protected.')
        self.assertEqual(self.mail.subject, 'This is the subject.')
        self.assertEqual(self.mail.host, 'smtp.thisdoesntexist.com')
        self.assertEqual(self.mail.username, 'myusername')
        self.assertEqual(self.mail.port, 25)
        self.assertIsNone(self.mail.attachment)

    def tearDown(self):
        self.mail = None
        del os.environ['MAIL_SENDER']
        del os.environ['MAIL_RECIPIENT']
        del os.environ['MAIL_BODY']
        del os.environ['MAIL_PASSWORD']
        del os.environ['MAIL_SUBJECT']
        del os.environ['MAIL_SERVER']
        del os.environ['MAIL_USERNAME']


class TestSettingEmails(unittest.TestCase):
    def setUp(self):
        self.mail = email.Mail()
        self.addrs_pass = ['test@test.com', 'test@test.org', 'test@test.gov', 'test@test.au']
        self.addrs_fail = ['nope.com', 'uhuh@me', 'notgonna@.pass', '@cant.wont', 'back.wards@com']

    def test_good_sender(self):
        for addr in self.addrs_pass:
            self.mail.sender = addr

    def test_bad_sender(self):
        for addr in self.addrs_fail:
            try:
                self.mail.sender = addr
                raise AttributeError('Oops, a valid attribute was found, and these should be invalid.')
            except Exception as e:
                self.assertIsInstance(e, email.InvalidEmailFormatError)

    def test_good_recipient(self):
        for addr in self.addrs_pass:
            self.mail.recipient = addr

    def test_bad_recipients(self):
        for addr in self.addrs_fail:
            try:
                self.mail.recipient = addr
                raise AttributeError('Oops, a valid attribute was found, and these should be invalid.')
            except Exception as e:
                self.assertIsInstance(e, email.InvalidEmailFormatError)

    def tearDown(self):
        self.mail = None


class TestMailTypeErrors(unittest.TestCase):
    def setUp(self):
        self.mail = email.Mail()

    def test_subject(self):
        for item in [4, {}, []]:
            try:
                self.mail.subject = item
                raise Exception
            except Exception as e:
                self.assertIsInstance(e, TypeError)

    def test_body(self):
        for item in [4, {}, []]:
            try:
                self.mail.body = item
                raise Exception
            except Exception as e:
                self.assertIsInstance(e, TypeError)

    def test_host(self):
        for item in [4, {}, []]:
            try:
                self.mail.host = item
                raise Exception
            except Exception as e:
                self.assertIsInstance(e, TypeError)

    def test_port(self):
        for item in ['nope', {}, []]:
            try:
                self.mail.port = item
                raise Exception
            except Exception as e:
                self.assertIsInstance(e, TypeError)

    def test_sender(self):
        for item in [4, {}, []]:
            try:
                self.mail.sender = item
                raise Exception
            except Exception as e:
                self.assertIsInstance(e, TypeError)

    def test_recipient(self):
        for item in [4, {}, []]:
            try:
                self.mail.sender = item
                raise Exception
            except Exception as e:
                self.assertIsInstance(e, TypeError)

    def test_username(self):
        for item in [4, {}, []]:
            try:
                self.mail.username = item
                raise Exception
            except Exception as e:
                self.assertIsInstance(e, TypeError)

    def test_password(self):
        for item in [4, {}, []]:
            try:
                self.mail.password = item
                raise Exception
            except Exception as e:
                self.assertIsInstance(e, TypeError)

    def test_tls(self):
        for item in [4, 'nope', {}, []]:
            try:
                self.mail.tls = item
                raise Exception
            except Exception as e:
                self.assertIsInstance(e, TypeError)

    def test_attachment(self):
        for item in [4, {}, []]:
            try:
                self.mail.attachment = item
                raise Exception
            except Exception as e:
                self.assertIsInstance(e, TypeError)

    def tearDown(self):
        self.mail = None


class TestValidMailAttributes(unittest.TestCase):
    def setUp(self):
        self.mail = email.Mail()

    def test_all_attrs(self):
        self.mail.sender = 'email@email.com'
        self.mail.recipient = 'mail@mail.com'
        self.mail.body = 'Email body.'
        self.mail.port = 20
        self.mail.password = 'supersecret'
        self.mail.subject = 'Mail subject.'
        self.mail.host = 'smtp.somedomain.com'
        self.mail.username = 'username'
        self.mail.tls = True

    def tearDown(self):
        self.mail = None


class TestAttachment(unittest.TestCase):
    def setUp(self):
        self.mail = email.Mail()
        files = [i for i in os.listdir() if os.path.isfile(i)]
        if files:
            self.file = files[0]
        else:
            raise FileNotFoundError('Unable to test TestAttachment: no files in current working directory.')
        self.valid_path_invalid_file = ''.join([os.getcwd().replace('\\', '/'), '/good-luck-finding-me.lmnop'])
        self.invalid_path = 'path/that/doesnt/exist/anywhere/'

    def test_valid_path(self):
        if self.file:
            self.mail.attachment = self.file
        else:
            raise FileNotFoundError('Unable to test TestAttachment.test_valid_path: no files in current working '
                                    'directory.')

    def test_valid_path_invalid_file(self):
        try:
            self.mail.attachment = self.valid_path_invalid_file
            raise Exception
        except Exception as e:
            self.assertIsInstance(e, FileNotFoundError)

    def test_invalid_path(self):
        try:
            self.mail.attachment = self.invalid_path
            raise Exception
        except Exception as e:
            self.assertIsInstance(e, FileNotFoundError)

    def tearDown(self):
        self.mail = None


class TestSendEmailWithoutSender(unittest.TestCase):
    def setUp(self):
        self.mail = email.Mail()

    def test_missing_sender(self):
        self.mail.recipient = 'mail@mail.com'
        self.mail.subject = 'subject'
        self.mail.host = 'host.host.host'
        self.mail.body = 'body'
        try:
            self.mail.send_mail()
            raise Exception
        except Exception as e:
            self.assertIsInstance(e, AttributeError)

    def tearDown(self):
        self.mail = None


class TestSendEmailWithoutRecipient(unittest.TestCase):
    def setUp(self):
        self.mail = email.Mail()

    def test_missing_recipient(self):
        self.mail.sender = 'mail@mail.com'
        self.mail.subject = 'subject'
        self.mail.host = 'host.host.host'
        self.mail.body = 'body'
        try:
            self.mail.send_mail()
            raise Exception
        except Exception as e:
            self.assertIsInstance(e, AttributeError)

    def tearDown(self):
        self.mail = None


class TestSendEmailWithoutSubject(unittest.TestCase):
    def setUp(self):
        self.mail = email.Mail()

    def test_missing_subject(self):
        self.mail.sender = 'mail@mail.com'
        self.mail.recipient = 'mail@mail.com'
        self.mail.host = 'host.host.host'
        self.mail.body = 'body'
        try:
            self.mail.send_mail()
            raise Exception
        except Exception as e:
            self.assertIsInstance(e, AttributeError)

    def tearDown(self):
        self.mail = None


class TestSendEmailWithoutBody(unittest.TestCase):
    def setUp(self):
        self.mail = email.Mail()

    def test_missing_body(self):
        self.mail.sender = 'mail@mail.com'
        self.mail.recipient = 'mail@mail.com'
        self.mail.host = 'host.host.host'
        self.mail.subject = 'subject'
        try:
            self.mail.send_mail()
            raise Exception
        except Exception as e:
            self.assertIsInstance(e, AttributeError)

    def tearDown(self):
        self.mail = None


class TestSendEmailWithoutHost(unittest.TestCase):
    def setUp(self):
        self.mail = email.Mail()

    def test_missing_host(self):
        self.mail.sender = 'mail@mail.com'
        self.mail.recipient = 'mail@mail.com'
        self.mail.subject = 'subject'
        self.mail.body = 'body'
        try:
            self.mail.send_mail()
            raise Exception
        except Exception as e:
            self.assertIsInstance(e, AttributeError)

    def tearDown(self):
        self.mail = None


class TestSendEmailTLSWithoutUsername(unittest.TestCase):
    def setUp(self):
        self.mail = email.Mail()

    def test_tls_missing_username(self):
        self.mail.sender = 'mail@mail.com'
        self.mail.recipient = 'mail@mail.com'
        self.mail.subject = 'subject'
        self.mail.body = 'body'
        self.mail.host = 'host.host.host'
        self.mail.tls = True
        self.mail.password = 'supersecret'
        try:
            self.mail.send_mail()
            raise Exception
        except Exception as e:
            self.assertIsInstance(e, AttributeError)

    def tearDown(self):
        self.mail = None


class TestSendEmailTLSWithoutPassword(unittest.TestCase):
    def setUp(self):
        self.mail = email.Mail()

    def test_tls_missing_password(self):
        self.mail.sender = 'mail@mail.com'
        self.mail.recipient = 'mail@mail.com'
        self.mail.subject = 'subject'
        self.mail.body = 'body'
        self.mail.host = 'host.host.host'
        self.mail.tls = True
        self.mail.username = 'username'
        try:
            self.mail.send_mail()
            raise Exception
        except Exception as e:
            self.assertIsInstance(e, AttributeError)

    def tearDown(self):
        self.mail = None


if __name__ == '__main__':
    unittest.main()
