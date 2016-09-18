# -*- coding: utf-8 -*-
# !/usr/bin/python
__author__ = 'Code_Cola'

import urllib
import urllib2
import cookielib
import socket
import re
import os
from time import *
from datetime import *
from bin.log import logging
from conf.global_config import *


class VisitError(Exception):
    pass


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
            raise VisitError
        return s


class OJAccess(Access):
    def __init__(self, oj):
        super(OJAccess, self).__init__(header=Headers[oj])
        self.oj = oj
        self.refresh_time = None

    def visit(self, url, post_data=None, referer=''):
        if self.refresh_time is not None and datetime.now() < self.refresh_time:
            sleep((self.refresh_time - datetime.now()).total_seconds())
            self.refresh_time = None
        s = super(OJAccess, self).visit(url, post_data, referer)
        if OJ_Decode[self.oj]:
            s = s.decode('gbk', 'ignore').encode('utf8')
        if NOT_Refresh[self.oj]:
            t = self.refresh(s)
            if t is not None:
                self.refresh_time = datetime.now() + timedelta(seconds=int(t))
                return self.visit(url, post_data, referer)
        if self.wrong_page(s):
            logging.warning("OJ Forbidden!!! html:\n" + s)
            raise VisitError
        return s

    def wrong_page(self, html):
        match = re.search(Forbidden[self.oj], html, re.M | re.I)
        return True if match else False

    def refresh(self, html):
        match = re.search(RE_Refresh[self.oj], html, re.M | re.I)
        return match.group(1) if match else None


class UserAccess(OJAccess):
    def __init__(self, oj, username, password):
        super(UserAccess, self).__init__(oj)
        self.username = username
        self.password = password
        self.postdata = Login_Data[self.oj]
        self.postdata[Login_Data_List[self.oj][0]] = username
        self.postdata[Login_Data_List[self.oj][1]] = password

    def login(self, cid=None):
        if cid is not None:
            url = Login_URL[self.oj] % cid
        else:
            url = Login_URL[self.oj]
        try:
            html = self.visit(url, self.postdata)
        except VisitError:
            logging.info("OJ:" + self.oj + " USER: " + self.username + " NOT Login!!!")
            return False
        if not self.judge_password(html):
            logging.warning("Login ERRER!!! No Such User!!!")
            return False
        else:
            if self.is_login(cid):
                logging.info("OJ:" + self.oj + " USER: " + self.username + " Logined")
                return True
            else:
                logging.info("OJ:" + self.oj + " USER: " + self.username + " NOT Login!!!")
                return False

    def is_login(self, cid=None):
        if cid is not None:
            url = OJ_Index[self.oj] % cid
        else:
            url = OJ_Index[self.oj]
        try:
            html = self.visit(url)
        except VisitError:
            return False
        match = re.search(NOT_Login[self.oj], html, re.M | re.I)
        return False if match else True

    def judge_password(self, html):
        match = re.search(Login_ERROR[self.oj], html, re.M | re.I)
        return False if match else True


class JudgeAccess(UserAccess):
    def __init__(self, oj, username, password, cid=None):
        super(JudgeAccess, self).__init__(oj, username, password)
        self.cid = cid
        self.login(cid)
        self.is_login(cid)

    def get_last_sid(self):
        if self.cid is not None:
            referer = OJ_Index[self.oj] % self.cid
            url = URL_Last_Submit[self.oj] % (self.cid, self.username)
        else:
            referer = OJ_Index[self.oj]
            url = URL_Last_Submit[self.oj] + self.username
        try:
            html = self.visit(url, referer=referer)
        except VisitError:
            return -1
        match = re.search(RE_Last_Submit[self.oj], html, re.M | re.I)
        return match.group(1) if match else -1


class NoSuchProblem(Exception):
    pass


class ProblemAccess(OJAccess):
    def visit(self, url, post_data=None, referer=''):
        s = super(ProblemAccess, self).visit(url, post_data, referer)
        match = re.search(RE_Problem[self.oj][0], s, re.M | re.I)
        if match:
            raise NoSuchProblem
        return s

    def save_img(self, url, problem_id=''):
        filename = url.split('/')[-1]
        path = os.path.join(STATIC_PATH, 'upload', self.oj, str(problem_id))
        make_dir(path)
        path = os.path.join(path, filename)
        if url[0:4] != 'http':
            if self.oj == 'hdu_std':
                url = OJ_Index['hdu'] + url
            else:
                url = OJ_Index[self.oj] + url
        try:
            urllib.urlretrieve(url, path)
        except:
            logging.warning("Get Image ERROR!!!")
        else:
            logging.info("Download image <%s> over" % (filename))


class ContestProblemAccess(JudgeAccess, ProblemAccess):
    def __init__(self, oj, username, password, cid):
        JudgeAccess.__init__(self, oj, username, password, cid)


def make_dir(path):
    if not os.path.exists(path):
        make_dir('/'.join(os.path.join(path.split('/')[:-1])))
        os.mkdir(path)
