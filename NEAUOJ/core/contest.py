# -*- coding:utf-8 -*-
# !/usr/bin/python

__author__ = 'Code_Cola'

import re
from Queue import Queue
import threading
from bin.log import logging
from bin.access import ContestProblemAccess, VisitError, NoSuchProblem
from bin.problem import ContestProblem
from db.mysql import MySQL, MySQLQueryError
from conf.global_config import *


class Contest(threading.Thread):
    def __init__(self, oj, username, password, cid, contest_id):
        super(Contest, self).__init__()
        self.oj = oj
        self.cid = cid
        self.username = username
        self.password = password
        self.contest_id = contest_id
        self.ac = ContestProblemAccess(oj, username, password, cid)
        self.mysql = MySQL()

    def test_contest(self):
        if not self.ac.is_login(self.cid):
            return False
        try:
            self.ac.visit(URL_Problem[self.oj] % (1001, self.cid))
        except VisitError:
            return False
        except NoSuchProblem:
            return False
        return True

    def get_problem_number(self):
        if not self.test_contest():
            return 0
        try:
            html = self.ac.visit(OJ_Index[self.oj] % self.cid)
        except VisitError:
            return 0
        return len(re.findall(r'class=table_text align=center', html, re.M | re.I))

    def run(self):
        problem_list = []
        sql = "SELECT in_problem_id FROM contest_contest_problem WHERE contest_id='%d'" % self.contest_id
        in_problem_id_list = self.mysql.query(sql)
        for x in in_problem_id_list:
            in_problem_id = x[0]
            sql = "SELECT problem_new_id, problem_id FROM contest_in_problem WHERE id='%d'" % in_problem_id
            probelm_new_id, problem_id = self.mysql.query(sql)[0]
            problem = ContestProblem(self.oj, self.username, self.password, self.cid, int(probelm_new_id) + 1001,
                                     problem_id)
            problem.run()
            problem_list.append([in_problem_id, problem_id])
        try:
            html = self.ac.visit(OJ_Index[self.oj] % self.cid)
        except VisitError:
            return
        match = re.search(r'<h1.*?>(.*?)</h1>', html, re.M | re.I)
        title = match.group(1) if match else None
        if title is not None:
            sql = "UPDATE contest_contest SET title='%s' WHERE id='%d'" % (title, self.contest_id)
            self.mysql.update(sql)
        match = re.search(r'Start Time : (.*?)&nbsp;?', html, re.M | re.I)
        start_time = match.group(1) if match else None
        if start_time is not None:
            sql = "UPDATE contest_contest SET start_time='%s' WHERE id='%d'" % (start_time, self.contest_id)
            self.mysql.update(sql)
        match = re.search(r'End Time : (.*?)<br>', html, re.M | re.I)
        end_time = match.group(1) if match else None
        if end_time is not None:
            sql = "UPDATE contest_contest SET end_time='%s' WHERE id='%d'" % (end_time, self.contest_id)
            self.mysql.update(sql)
        for i in problem_list:
            in_problem_id = i[0]
            problem_id = i[1]
            sql = "SELECT title FROM problem_problem WHERE id='%d'" % problem_id
            title = self.mysql.query(sql)[0][0]
            title = self.mysql.db.escape_string(title)
            sql = "UPDATE contest_in_problem SET title = '%s' WHERE id = '%d'" % (title, in_problem_id)
            self.mysql.update(sql)
