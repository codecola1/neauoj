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

    def test_problem(self, oj, problem_id):
        return self.send("2 %s %s" % (oj, problem_id))

    def download_problem(self, oj, problem_id, pid):
        return self.send("1 %s %s %d" % (oj, problem_id, pid))

    def test_user(self, oj, username, password):
        return self.send("3 %s %s %s" % (oj, username, password))

    def update_user(self, sid):
        return self.send("4 %s" % sid)

    def test_contest(self, cid):
        from core.models import Judge_account
        account = Judge_account.objects.get(oj='hdu_std')
        return self.send("5 hdu_std %s %s %d" % (account.username, account.password, cid))

    def clone_contest(self, cid, contest_id):
        from core.models import Judge_account
        account = Judge_account.objects.get(oj='hdu_std')
        return self.send("6 hdu_std %s %s %d %d" % (account.username, account.password, cid, contest_id))
