#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-

"""Email module.

Classes:

    Mail: SMTP email class.

    Error, InvalidEmailFormatError (used for validation) of the Mail class.


Functions:

    validate_email(email_address)
"""

import os
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


# custom Error classes
class Error(Exception):
    """Base Error class."""
    pass


class InvalidEmailFormatError(Error):
    """This error is raised if an invalid email format is encountered."""
    def __init__(self, message):
        self.message = message


def validate_email(email_address):
    """This function returns True if an email is valid and False if it isn't."""

    if isinstance(email_address, str):

        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        # for custom mails use: '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$

        if re.search(regex, email_address):
            return True
        else:
            return False

    else:
        raise TypeError('Email addresses must be strings.')


class Mail:
    """The Mail class contains attributes and methods associated with sending SMTP emails.

    Attributes
    ----------
        __attachment:
            The file path for an attachment.

        __body:
            Validated as a string. Text to use for the email body.

        host:
            The SMTP email host to send the email.

        __password:
            (Optional): The password if needed for TLS protocol.

        __port:
            Default 25: The port for the SMTP host.

        __recipient:
            Validated as having a valid email format: The email address of the email recipient.

        __sender:
            Validated as having a valid email format: The email address of the email sender.

        __subject:
            Validated as a string. Text to use as the subject of the email message.

        tls:
            Validated as Boolean: Default False: Whether or not to use TLS protocol for the email.

        username:
            (Optional): A string of text for the username of the email account to verify for TLS encryption.



    Methods
    -------
        send_mail():
            Sends an email to from the sender to the recipient set in the Mail object.

    """

    def __init__(self):

        self.__sender = os.getenv('MAIL_SENDER')
        self.__recipient = os.getenv('MAIL_RECIPIENT')
        self.__body = os.getenv('MAIL_BODY')
        self.__port = os.getenv('MAIL_PORT', 25)
        self.__password = os.getenv('MAIL_PASSWORD')
        self.__subject = os.getenv('MAIL_SUBJECT')
        self.__attachment = None
        self.__host = os.getenv('MAIL_SERVER')
        self.__username = os.getenv('MAIL_USERNAME')
        self.__tls = os.getenv('MAIL_TLS', False)

    # define protected properties
    # sender property
    @property
    def sender(self):
        return self.__sender

    @sender.setter
    def sender(self, value):
        if validate_email(value):
            self.__sender = value
        else:
            raise InvalidEmailFormatError(f'{value} is not a valid email address format.')

    # recipient property
    @property
    def recipient(self):
        return self.__recipient

    @recipient.setter
    def recipient(self, value):
        if validate_email(value):
            self.__recipient = value
        else:
            raise InvalidEmailFormatError(f'{value} is not a valid email address format.')

    # body validation
    @property
    def body(self):
        return self.__body

    @body.setter
    def body(self, value):
        if isinstance(value, str):
            self.__body = value
        else:
            raise TypeError('Email body must be a string.')

    # port property
    @property
    def port(self):
        return self.__port

    @port.setter
    def port(self, value):
        if isinstance(value, int):
            self.__port = value
        else:
            raise TypeError(f'Port number must be an integer. You entered {value}.')

    # attachment property
    @property
    def attachment(self):
        return self.__attachment

    @attachment.setter
    def attachment(self, value):
        if isinstance(value, str):
            if os.path.exists(value):
                if os.path.isfile(value):
                    self.__attachment = value
                else:
                    raise FileNotFoundError(f'File {value} not found at specified path.')
            else:
                raise FileNotFoundError(f'Unable to locate path. Current working directory is {os.getcwd()}.')
        else:
            raise TypeError('attachment must be a string file path.')

    @property
    def username(self):
        return self.__username

    @username.setter
    def username(self, value):
        if isinstance(value, str):
            self.__username = value
        else:
            raise TypeError('username must be a string')

    @property
    def password(self):
        return 'Value is protected.'

    @password.setter
    def password(self, value):
        if isinstance(value, str):
            self.__password = value
        else:
            raise TypeError('password must be a string')

    # subject property
    @property
    def subject(self):
        return self.__subject

    @subject.setter
    def subject(self, value):
        if isinstance(value, str):
            self.__subject = value
        else:
            raise TypeError('subject must be a string')

    # host property
    @property
    def host(self):
        return self.__host

    @host.setter
    def host(self, value):
        if isinstance(value, str):
            self.__host = value
        else:
            raise TypeError('host must be a string')

    # tls property
    @property
    def tls(self):
        return self.__tls

    @tls.setter
    def tls(self, value):
        if isinstance(value, bool):
            self.__tls = value
        else:
            raise TypeError('tls must be boolean')

    # send mail method
    def send_mail(self):
        """The mail object properties must all be valid prior to calling this method.

        Sends an SMTP email using the defined attributes of the mail object."""

        if not self.__sender:
            raise AttributeError('The "sender" attribute must be set to send an email.')
        if not self.__recipient:
            raise AttributeError('The "recipient" attribute must be set to send an email.')
        if not self.__subject:
            raise AttributeError('The "subject" attribute must be set to send an email.')
        if not self.__body:
            raise AttributeError('The "body" attribute must be set to send an email.')
        if not self.__host:
            raise AttributeError('The "host" attribute must be set to send an email.')
        if not self.__port:
            raise AttributeError('The "port" attribute must be set to send an email.')
        if self.__tls:
            if not self.__username or not self.__password:
                raise AttributeError('The "username" and "password" attributes must be set to send TLS emails.')

        # define the message
        message = MIMEMultipart()
        message['From'] = self.__sender
        message['To'] = self.__recipient
        message['Subject'] = self.__subject
        message.attach(MIMEText(self.__body, 'plain'))

        # format and set the attachment if present
        if self.__attachment:
            # set the filename
            if '\\' in self.__attachment:
                self.__attachment.replace('\\', '/')
            if '/' in self.__attachment:
                idx = self.__attachment.rfind('/') + 1
                filename = self.__attachment[idx:]
            else:
                filename = self.__attachment

            # read in the attachment
            with open(self.__attachment, 'rb') as file:
                payload = MIMEBase('application', 'octate-stream')
                payload.set_payload(file.read())
                encoders.encode_base64(payload)
                payload.add_header('Content-Disposition', 'attachment', filename=filename)
                message.attach(payload)

        with smtplib.SMTP(self.__host, self.__port) as smtp:
            if self.tls:
                if not self.__username or not self.__password:
                    raise AttributeError(
                        'The "username" and "password" attributes must be set to send TLS emails.')
                smtp.starttls()
                smtp.login(self.__username, self.__password)
            text = message.as_string()
            smtp.sendmail(self.__sender, self.__recipient, text)
            smtp.close()
            smtp.quit()
