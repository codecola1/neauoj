# -*- coding:utf-8 -*-
# !/usr/bin/python

__author__ = 'Code_Cola'

import stat
import socket
import os
from conf.global_config import Socket_PATH


class Connect:
    def __init__(self):
        self.server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.connection = None
        if os.path.exists(Socket_PATH):
            os.unlink(Socket_PATH)
        self.server.bind(Socket_PATH)
        os.chmod(Socket_PATH, stat.S_IRWXU | stat.S_IRGRP | stat.S_IROTH)
        self.server.listen(0)

    def get_message(self):
        self.connection, address = self.server.accept()
        message = self.connection.recv(1024).split(' ')
        return message

    def receive_message(self, message='Receive!'):
        self.connection.send(message)
        self.connection.close()

    def __del__(self):
        self.server.close()
