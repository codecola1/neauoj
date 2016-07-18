# -*- coding:utf-8 -*-
# !/usr/bin/python

__author__ = 'Code_Cola'

import re
import threading
import HTMLParser
import MySQLdb
from datetime import date
from access import Access
from support.mysql_join import MySQL

from config import *


def test_account(oj, username, password):
    ac = Access(oj, username, password)
    return ac.logined()


def get_last_rid(oj, username):
    ac = Access(oj=oj)
    url = user_status[oj] % ('', username)
    html = ac.get_html(url=url)
    match = re.search(user_last_rid[oj], html, re.M)
    return match.group(1)


class Update(threading.Thread):
    def __init__(self, user_id):
        threading.Thread.__init__(self)
        self.user_id = user_id
        self.mysql = MySQL()

    def run(self):
        data = self.mysql.query("SELECT oj_account_id FROM users_info_oj_account WHERE info_id = '%s'" % self.user_id)
        for id in data:
            info = self.mysql.query(
                "SELECT oj, username, password, defunct, last_rid, is_using FROM users_oj_account WHERE id = '%s'" % id[
                    0])
            oj, username, password, defunct, last_rid, is_using = info[0]
            if not defunct:
                ret = get_last_rid(oj, username)
                if ret != last_rid and not is_using:
                    updata_user(id[0], oj, username, password, ret, last_rid, self.user_id, self.mysql)


def updata_user(id, oj, username, password, last_rid, user_last_rid, user_id, mysql):
    sql = "UPDATE users_oj_account SET is_using = '1', updating = '0' WHERE id = '%s'" % id
    mysql.update(sql)
    ac = Access(oj, username, password)
    if ac.logined():
        status = []
        url = user_status[oj] % ('', username)
        html = ac.get_html(url=url)
        match = re.compile(get_status[oj], re.M | re.I | re.S)
        result = match.findall(html)
        i = 0
        while result[i][0] != user_last_rid:
            p_id = mysql.query(
                "SELECT id FROM problem_problem WHERE oj = '%s' AND problem_id = '%s'" % (oj, result[i][3]))
            if not p_id:
                mysql.update(
                    "INSERT INTO problem_problem (oj, problem_id, defunct, judge_type, date, title, description, input, output, sample_input, sample_output, hint, source, submit, solved, type, memory_limit_c, memory_limit_java, time_limit_c, time_limit_java, data_number) VALUES('%s', '%s', '1', '1', '%s', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '0', '0', ' ', '0', '0', '0', '0', '-1')" % (
                        oj, result[i][3], date.today()))
                p_id = mysql.get_id()
            else:
                p_id = p_id[0][0]
            status.append(
                [result[i][2], p_id, result[i][4], result[i][5], result[i][6], result[i][7], result[i][1],
                 result[i][0]])
            i += 1
            if i == len(result):
                url = user_status[oj] % (int(result[i - 1][0]) - 1, username)
                html = ac.get_html(url=url)
                result = match.findall(html)
                if len(result) == 0:
                    break
                i = 0
        l = len(status)
        j = 1
        for i in status:
            code = get_code(ac.get_html(url=get_code_url[oj] % i[7]), oj)
            sql = "INSERT INTO status_solve (status, submit_time, problem_id, use_time, use_memory, length, language, code, user_id) VALUES('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (
                i[0], i[6], i[1], i[2], i[3], i[4], i[5], code, user_id)
            mysql.update(sql)
            solve_id = mysql.get_id()
            if i[0] == 'Compilation Error':
                ce_info_t = get_ce_info(ac.get_html(url=get_ce_url[oj] % i[7]), oj)
                sql = "INSERT INTO status_ce_info (info, solve_id) VALUES('%s', '%s')" % (ce_info_t, solve_id)
                mysql.update(sql)
            sql = "SELECT ac FROM users_submit_problem WHERE user_id = '%s' AND problem_id = '%s'" % (user_id, i[1])
            result = mysql.query(sql)
            if result:
                if i[0] == 'Accepted' and int(result[0][0]) == 0:
                    sql = "UPDATE users_submit_problem SET ac = '1' WHERE user_id = '%s' AND problem_id = '%s'" % (
                        user_id, i[1])
                    mysql.update(sql)
            else:
                sql = "INSERT INTO users_submit_problem (ac, problem_id, user_id) VALUES('%s', '%s', '%s')" % (
                    '1' if i[0] == 'Accepted' else '0', i[1], user_id)
                mysql.update(sql)
            sql = "UPDATE users_oj_account SET updating = '%d' WHERE id = '%s'" % (int(j / float(l) * 100), id)
            mysql.update(sql)
            j += 1
        sql = "UPDATE users_oj_account SET is_using = '0', last_rid = '%s' WHERE id = '%s'" % (last_rid, id)
        mysql.update(sql)


def get_code(html, oj):
    match = re.search(get_code_re[oj], html, re.M | re.DOTALL)
    try:
        code = unicode(match.group(1), "utf-8")
    except:
        code = ''
    html_parser = HTMLParser.HTMLParser()
    return MySQLdb.escape_string(html_parser.unescape(code))


def get_ce_info(html, oj):
    t = re.search(get_ce_re[oj], html, re.M | re.I | re.S)
    try:
        string = t.group(1)
    except:
        string = ''
    html_parser = HTMLParser.HTMLParser()
    return MySQLdb.escape_string(html_parser.unescape(string))
