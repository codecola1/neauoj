# -*- coding:utf-8 -*-
# !/usr/bin/python

__author__ = 'Code_Cola'


import socket

class Connect:
    def __init__(self):
        self.client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.sock = "/tmp/neauoj.sock"

    def send(self, s):
        self.client.connect(self.sock)
        self.client.send(str(s))
        receive = self.client.recv(1024)
        self.client.close()
        return receive

    def judge_start(self):
        self.send("0 0")

    def judge_stop(self):
        self.send("0 1")

    def judge_restart(self):
        self.send("0 2")

    def judge_code(self, sid):
        return self.send("0 3 " + str(sid) + " 0")

    def rejudge_code(self, sid):
        return self.send("0 3 " + str(sid) + " 1")
