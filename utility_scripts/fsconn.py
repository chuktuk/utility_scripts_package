#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-


"""fsconn module for file server connections."""


import paramiko
import os


class FSConnection:
    def __init__(self, env='development'):
        if env == 'production':
            self.__keyfilepath = os.getenv('SSH_KEYPATH')
            self.__host = os.getenv('SSH_HOST')
            self.__username = os.getenv('SSH_USERNAME')
        else:
            self.__keyfilepath = os.getenv('SSH_DEV_KEYPATH')
            self.__host = os.getenv('SSH_DEV_HOST')
            self.__username = os.getenv('SSH_DEV_USERNAME')
        self.__port = os.getenv('SSH_PORT', 22)
        self.__key = None

    @property
    def keyfilepath(self):
        return 'Protected data.'

    @keyfilepath.setter
    def keyfilepath(self, value):
        if isinstance(value, str):
            if os.path.exists(value):
                if os.path.isfile(value):
                    self.__keyfilepath = value
                else:
                    raise FileNotFoundError(f'File {value} not found at specified path.')
            else:
                raise FileNotFoundError(f'Unable to locate key file path. Current working directory is {os.getcwd()}.')
        else:
            raise TypeError('keyfilepath must be a string providing the path to the private key file.')

    @property
    def host(self):
        return 'Protected data.'

    @host.setter
    def host(self, value):
        if isinstance(value, str):
            self.__host = value
        else:
            raise TypeError('The "host" attribute must be a string.')

    @property
    def username(self):
        return 'Protected data.'

    @username.setter
    def username(self, value):
        if isinstance(value, str):
            self.__username = value
        else:
            raise TypeError('The "username" attribute must be a string.')

    @property
    def port(self):
        return self.__port

    @port.setter
    def port(self, value):
        if isinstance(value, int):
            self.__port = value
        else:
            raise TypeError('The "port" attribute must be an integer. Have you tried 22?')

    def set_rsa_key(self):
        if self.__keyfilepath:
            if os.path.exists(self.__keyfilepath):
                if os.path.isfile(self.__keyfilepath):
                    self.__key = paramiko.RSAKey.from_private_key_file(self.__keyfilepath)
                else:
                    raise FileNotFoundError(f'File {self.__keyfilepath} not found at specified path.')
            else:
                raise FileNotFoundError(f'Unable to locate key file path. Current working directory is {os.getcwd()}.')
        else:
            raise AttributeError('Please set the "keyfilepath" attribute with the path to the SSH private key.')

    def get_sftp(self):
        if self.__key:
            if isinstance(self.__key, paramiko.rsakey.RSAKey):
                ssh_client = paramiko.SSHClient()
                ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh_client.connect(hostname=self.__host, username=self.__username, pkey=self.__key)
                ftp_client = ssh_client.open_sftp()
            else:
                raise TypeError('The rsa key must be properly set to call .get_sftp(). Did you set the keyfilepath '
                                'attribute and call .set_rsa_key()?')
        else:
            raise AttributeError('Please set the "keyfilepath" attribute with the path to the SSH private key then '
                                 'call the .set_rsa_key() method before calling .get_sftp().')

        return ftp_client
