# -*- coding:utf-8 -*-
# !/usr/bin/python

__author__ = 'Code_Cola'

import re
from HTMLParser import HTMLParser
from bin.log import Log
from db.mysql import MySQL
from bin.access import ProblemAccess
from conf.global_config import *

logging = Log()
img = []


class Problem(object):
    def __init__(self, oj, problem_id, pid):
        self.mysql = MySQL()
        self.oj = oj
        self.problem_id = problem_id
        self.pid = pid
        self.ac = ProblemAccess(oj)
        global img
        img = []

    def find_img(self, s):
        parser = IMGParser()
        parser.feed(s)
        for i in img:
            i = i.replace('../', '')
            self.ac.save_img(i if i[0] == '/' or i[0] == 'h' else '/' + i, self.problem_id)

    def run(self):
        html = self.ac.visit(URL_Problem[self.oj] + str(self.problem_id))
        title = use_re(RE_Problem[self.oj][1], html)
        if self.oj == 'poj':
            time_limit_c = use_re(RE_Problem[self.oj][2], html)
            memory_limit_c = use_re(RE_Problem[self.oj][3], html)
            time_limit_java = str(2 * int(time_limit_c))
            memory_limit_java = memory_limit_c
        else:
            time_limit_java, time_limit_c = use_re(RE_Problem[self.oj][2], html, 2)
            memory_limit_java, memory_limit_c = use_re(RE_Problem[self.oj][3], html, 2)
        path = '/upload/' + self.oj + "/" + str(self.problem_id) + "/"
        path = path.encode("utf-8")
        description = use_re(RE_Problem[self.oj][4], html)
        problem_input = use_re(RE_Problem[self.oj][5], html)
        problem_output = use_re(RE_Problem[self.oj][6], html)
        s_input = use_re(RE_Problem[self.oj][7], html)
        s_output = use_re(RE_Problem[self.oj][8], html)
        hint = use_re(RE_Problem[self.oj][9], html)
        self.find_img(description + problem_input + problem_output + hint)
        if hint:
            if self.oj == 'hdu':
                s_output = s_output[0:-4]
            hint = re.sub(IMG_Replace[self.oj], path, hint.replace('../', ''))
        description = re.sub(IMG_Replace[self.oj], path, description.replace('../', ''))
        problem_input = re.sub(IMG_Replace[self.oj], path, problem_input.replace('../', ''))
        problem_output = re.sub(IMG_Replace[self.oj], path, problem_output.replace('../', ''))
        source = use_re(RE_Problem[self.oj][10], html)
        sql = """
              UPDATE problem_problem SET
                title='%s',
                time_limit_c='%s',
                time_limit_java='%s',
                memory_limit_c='%s',
                memory_limit_java='%s',
                description='%s',
                input='%s',
                output='%s',
                sample_input='%s',
                sample_output='%s',
                hint='%s',
                source='%s',
                defunct=100
                WHERE id='%s'
              """ % (
            self.mysql.db.escape_string(title),
            self.mysql.db.escape_string(time_limit_c),
            self.mysql.db.escape_string(time_limit_java),
            self.mysql.db.escape_string(memory_limit_c),
            self.mysql.db.escape_string(memory_limit_java),
            self.mysql.db.escape_string(description),
            self.mysql.db.escape_string(problem_input),
            self.mysql.db.escape_string(problem_output),
            self.mysql.db.escape_string(s_input),
            self.mysql.db.escape_string(s_output),
            self.mysql.db.escape_string(hint),
            self.mysql.db.escape_string(source),
            self.pid
        )
        self.mysql.update(sql)
        logging.info("Download Problem: " + self.oj + "-" + str(self.problem_id) + " Info Over")


class IMGParser(HTMLParser):
    global img

    def handle_starttag(self, tag, attrs):
        if tag == 'img':
            for attr in attrs:
                if attr[0] == 'src':
                    img.append(attr[1])


def use_re(rs, data, n=1):
    match = re.search(rs, data, re.M | re.I | re.DOTALL)
    if match:
        if n == 1:
            return match.group(1)
        ret = []
        for i in range(1, n + 1):
            ret.append(match.group(i))
        return ret
    else:
        return "" * n
