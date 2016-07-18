# -*- coding:utf-8 -*-
# !/usr/bin/python

__author__ = 'Code_Cola'

from bin.log import logging
from bin.access import JudgeAccess
from db.mysql import MySQL
from time import sleep
from conf.global_config import *
import re
import base64


class JudgeSubmitError(Exception):
    pass


class Judge(object):
    def __init__(self, language, code):
        self.language = language
        self.code = code

    def judge(self):
        """
        判题函数，返回评判结果。
        :return:
        """


class LocalJudge(Judge):
    def __init__(self, language, code):
        super(LocalJudge, self).__init__(language, code)


class VirtualJudge(Judge):
    def __init__(self, username, password, last_sid, language, code, oj, problem_id, sid, cid=None):
        super(VirtualJudge, self).__init__(language, code)
        if oj == 'poj' or oj == 'hdu_std':
            self.code = base64.encodestring(self.code)
        self.oj = oj
        self.pid = problem_id
        self.last_sid = last_sid
        self.username = username
        self.sid = sid
        self.cid = cid
        self.mysql = MySQL()
        self.ac = JudgeAccess(oj, username, password, cid)

    def judge(self):
        self.submit()
        sleep(0.5)
        try:
            self.search_sid()
        except JudgeSubmitError:
            status = "Judge ERROR"
            use_time = 0
            use_memory = 0
            self.update(status, use_time, use_memory)
            return
        status = self.refresh_status()
        while self.refresh_again(status[0]):
            sleep(0.2)
            status = self.refresh_status()
        if self.is_ce(status):
            if self.cid is not None:
                url = URL_CE[self.oj] % (self.cid, self.rid)
            else:
                url = URL_CE[self.oj] + self.rid
            html = self.ac.visit(url)
            t = re.search(RE_Get_CE[self.oj], html, re.M | re.I | re.S)
            ce_info = t.group(1)
            self.save_ce(ce_info)

    def all_ready(self):
        return self.ac.is_login(self.cid)

    def submit(self):
        if self.cid is not None:
            url = URL_Submit[self.oj] % self.cid
            referer = URL_Referer[self.oj] % (self.cid, int(self.pid))
        else:
            url = URL_Submit[self.oj]
            referer = URL_Referer[self.oj] + str(self.pid)
        postdata = Submit_POST_Data[self.oj]
        postdata[Submit_POST_Data_List[self.oj][0]] = self.pid
        postdata[Submit_POST_Data_List[self.oj][1]] = VJ_Language_Map[self.oj][self.language]
        postdata[Submit_POST_Data_List[self.oj][2]] = self.code
        self.ac.visit(url, postdata, referer)

    def search_sid(self):
        sid = self.ac.get_last_sid()
        if int(sid) != int(self.last_sid):
            self.last_sid = sid
        else:
            raise JudgeSubmitError

    def refresh_status(self):
        if self.cid is not None:
            url = URL_Status[self.oj] % (self.cid, self.username)
        else:
            url = URL_Status[self.oj] + self.username
        html = self.ac.visit(url)
        match = re.search(RE_Judge_Status[self.oj] % self.last_sid, html, re.M | re.I | re.S)
        if match:
            status = match.group(1)
            use_time = match.group(2)
            use_memory = match.group(3)
        else:
            status = "Judge ERROR"
            use_time = 0
            use_memory = 0
        self.update(status, use_time, use_memory)
        return status, use_time, use_memory

    def refresh_again(self, s):
        status_list = [
            'Queuing',
            'Compiling',
            'Running',
            'Running & Judging',
            'Waiting',
        ]
        for i in status_list:
            if s == i:
                return True
        return False

    def is_ce(self, s):
        return s == 'Compilation Error'

    def update(self, status, use_time, use_memory):
        self.mysql.update(
            "UPDATE status_solve SET status = '%s', use_time = '%s', use_memory = '%s' WHERE id = '%s'" % (
                status, use_time, use_memory, self.sid
            )
        )

    def save_ce(self, ce_info):
        sql = "SELECT info FROM status_ce_info WHERE solve_id = '%s'" % self.sid
        result = self.mysql.query(sql)
        if result:
            sql = "UPDATE status_ce_info SET info = '%s' WHERE solve_id = '%s'" % (ce_info, self.sid)
            self.mysql.update(sql)
        else:
            sql = "INSERT INTO status_ce_info (info, solve_id) VALUES('%s', '%s')" % (ce_info, self.sid)
            self.mysql.update(sql)


class Judgeneau(LocalJudge):
    pass


class Judgehdu(VirtualJudge):
    pass


class Judgehdu_std(VirtualJudge):
    pass


class Judgepoj(VirtualJudge):
    pass
