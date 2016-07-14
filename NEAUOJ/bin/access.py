# -*- coding: utf-8 -*-
# !/usr/bin/python
__author__ = 'Code_Cola'

import urllib
import urllib2
import cookielib
import socket
import re
import os

from bin.log import Log
from conf.global_config import *

logging = Log()


class Access(object):
    def __init__(self, header=None):
        self.cookie = cookielib.CookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookie))
        self.header = None
        self.header = header if header else {}

    def visit(self, url, post_data=None, referer=''):
        header = self.header
        if referer:
            header['Referer'] = referer
        if post_data:
            post_data = urllib.urlencode(post_data)
        req = urllib2.Request(url=url, headers=header, data=post_data)
        try:
            s = self.opener.open(req).read()
        except urllib2.URLError, e:
            logging.warning("Get HTML ERROR!!!" + str(e.reason))
            return ''
        else:
            logging.info("get_html:" + url)
            return s.decode('gbk', 'ignore').encode('utf8') if OJ_Decode[self.oj] else s


class JudgeAccess(Access):
    def __init__(self, oj, username, password):
        super(JudgeAccess, self).__init__(header=Headers[oj])
        self.oj = oj
        self.username = username
        self.password = password
        self.postdata = Login_Data[self.oj]
        self.postdata[Login_Data_List[self.oj][0]] = username
        self.postdata[Login_Data_List[self.oj][1]] = password
        self.login()

    def visit(self, url, post_data=None, referer=''):
        s = super(JudgeAccess, self).visit(url, post_data, referer)
        match = re.search(Forbidden[self.oj], s, re.M)
        return "" if match else s

    def login(self):
        url = Login_URL[self.oj]
        html = self.visit(url, self.postdata)
        if not self.judge_password(html):
            logging.warning("Login ERRER!!! No Such User!!!")
            return False
            # sql = "UPDATE core_judge_account SET defunct = '1' WHERE id = '%s'" % (self.account_id)
            # Connect.query(sql)
        else:
            if self.is_login():
                logging.info("OJ:" + self.oj + " USER: " + self.username + " Logined")
                return True
            else:
                logging.info("OJ:" + self.oj + " USER: " + self.username + " NOT Login!!!")
                return False

    def get_last_sid(self):
        url = URL_Last_Submit[self.oj] + self.username
        html = self.visit(url, referer=OJ_Index[self.oj])
        match = re.search(RE_Last_Submit[self.oj], html, re.M)
        return match.group(1) if match else -1

    def is_login(self):
        url = OJ_Index[self.oj]
        html = self.visit(url)
        match = re.search(NOT_Login[self.oj], html, re.M)
        return False if match else True

    def judge_password(self, html):
        match = re.search(Login_ERROR[self.oj], html, re.M)
        return False if match else True


class ProblemAccess(Access):
    def __init__(self, oj):
        super(ProblemAccess, self).__init__(header=Headers[oj])
        self.oj = oj

    def visit(self, url, post_data=None, referer=''):
        s = super(ProblemAccess, self).visit(url, post_data, referer)
        match = re.search(RE_Problem[self.oj][0], s, re.M)
        return "" if match else s

    def save_img(self, url, problem_id=''):
        filename = url.split('/')[-1]
        path = os.path.join(STATIC_PATH, 'upload', self.oj, str(problem_id))
        make_dir(path)
        path = os.path.join(path, filename)
        if url[0:4] != 'http':
            url = OJ_Index[self.oj] + url
        try:
            urllib.urlretrieve(url, path)
        except:
            logging.warning("Get Image ERROR!!!")
        else:
            logging.info("Download image <%s> over" % (filename))


def make_dir(path):
    if not os.path.exists(path):
        make_dir('/'.join(os.path.join(path.split('/')[:-1])))
        os.mkdir(path)
