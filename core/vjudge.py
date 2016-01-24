# coding=utf-8
__author__ = 'Code_Cola'

from access import Access
from support.mysql_join import Connect
from time import sleep
import re

from config import *


class Vjudge:
    def __init__(self, sid, username, password, last_result):
        self.mysql = Connect()
        self.sid = sid
        self.get_info(sid)
        self.username = username
        self.ac = Access(self.oj, username, password)
        self.ce_info = ''
        self.last_result = last_result

    def get_info(self, sid):
        result = self.mysql.query("SELECT problem_id, language, code, user_id FROM status_solve WHERE id = '%s'" % sid)
        self.problem_id = result[0][0]
        self.language = result[0][1]
        self.code = result[0][2]
        self.uid = result[0][3]
        result = self.mysql.query("SELECT oj, problem_id FROM problem_problem WHERE id = '%s'" % self.problem_id)
        self.oj = result[0][0]
        self.pid = result[0][1]

    def submit(self):
        url = url_submit[self.oj]
        referer = url_referer[self.oj] + self.pid
        postdata = post_data[self.oj]
        postdata[judge_listmap[self.oj][0]] = self.pid
        postdata[judge_listmap[self.oj][1]] = language_map[self.oj][self.language]
        postdata[judge_listmap[self.oj][2]] = self.code
        self.ac.get_html(url, postdata, referer)

    def hdu_get_status(self):
        if not self.rid:
            url = url_status[self.oj][0]
            html = self.ac.get_html(url)
            match = re.search(re_string[self.oj][0] % self.username, html, re.M | re.I | re.S)
            s = match.group()
            self.rid = re.findall(re_string[self.oj][1], s, re.M | re.I | re.S)[-1]
        url = url_status[self.oj][1] + self.rid
        html = self.ac.get_html(url)
        match = re.search(re_string[self.oj][2] % self.rid, html, re.M | re.I | re.S)
        if match.group(1) == 'Compilation Error':
            url = url_ce[self.oj] + self.rid
            html = self.ac.get_html(url)
            t = re.search(re_string[self.oj][3], html, re.M | re.I | re.S)
            self.ce_info = t.group(1)
        return match.group(1), match.group(2), match.group(3)

    def hdu_again(self, s):
        if s == 'Queuing' or s == 'Compiling' or s == 'Running':
            return True
        return False

    def run(self):
        self.submit()
        self.rid = ''
        sleep(0.5)
        o = eval('self.' + self.oj + '_get_status')()
        self.mysql.update(
            "UPDATE status_solve SET status = '%s', use_time = '%s', use_memory = '%s' WHERE id = '%s'" % (
                o[0], o[1], o[2], self.sid))
        sleep(0.2)
        while eval('self.' + self.oj + '_again')(o[0]):
            o = eval('self.' + self.oj + '_get_status')()
            self.mysql.update(
                "UPDATE status_solve SET status = '%s', use_time = '%s', use_memory = '%s' WHERE id = '%s'" % (
                    o[0], o[1], o[2], self.sid))
            sleep(0.2)
            # print o
        if self.ce_info:
            sql = "SELECT info FROM status_ce_info WHERE solve_id = '%s'" % self.sid
            result = self.mysql.query(sql)
            if result:
                sql = "UPDATE status_ce_info SET info = '%s' WHERE solve_id = '%s'" % (self.ce_info, self.sid)
                self.mysql.update(sql)
            else:
                sql = "INSERT INTO status_ce_info (info, solve_id) VALUES('%s', '%s')" % (self.ce_info, self.sid)
                self.mysql.update(sql)
        sql = "SELECT ac FROM users_submit_problem WHERE user_id = '%s' AND problem_id = '%s'" % (self.uid, self.problem_id)
        result = self.mysql.query(sql)
        if result:
            if o[0] == 'Accepted' and int(result[0][0]) == 0:
                sql = "UPDATE users_submit_problem SET ac = '1' WHERE user_id = '%s' AND problem_id = '%s'" % (
                    self.uid, self.problem_id)
                self.mysql.update(sql)
        else:
            sql = "INSERT INTO users_submit_problem (ac, problem_id, user_id) VALUES('%s', '%s', '%s')" % (
            '1' if o[0] == 'Accepted' else '0', self.problem_id, self.uid)
            self.mysql.update(sql)
            # if o[0] == 'Accepted' and not self.last_result:
            #     self.mysql.update("UPDATE problem_problem SET solved = solved + '1' WHERE id = '%s'" % self.pid)
            #     self.mysql.update("UPDATE users_info SET solve = solve + '1' WHERE id = '%s'" % self.uid)
