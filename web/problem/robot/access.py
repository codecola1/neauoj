# coding=utf-8
# !/usr/bin/python
__author__ = 'Code_Cola'

import urllib
import urllib2
import cookielib
import re
import os

from web.settings import STATIC_PATH
import logging
from web.access_parameter import *

logger = logging.getLogger(__name__)

class Access:
    def __init__(self, oj='', username='', password=''):
        self.cookie = cookielib.CookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookie))
        self.oj = oj
        self.header = Headers[self.oj]
        if username:
            self.username = username
            self.postdata = login_data[self.oj]
            self.postdata[Listmap[self.oj][0]] = username
            self.postdata[Listmap[self.oj][1]] = password
            self.login()

    def get_html(self, url, postdata={}, referer=''):
        # if self.username and not self.logined():需要修改
        #     self.login()
        header = self.header
        if referer:
            header['Referer'] = referer
        req = urllib2.Request(url=url, headers=header,
                              data=None if not len(postdata) else urllib.urlencode(postdata))
        try:
            s = self.opener.open(req).read()
            if decode[self.oj]:
                s = s.decode('gbk', 'ignore').encode('utf8')
        except urllib2.URLError, e:
            logging.warning("Get HTML ERROR!!!" + str(e.reason))
            return ''
        else:
            logging.info("get_html:" + url)
            return s

    def judge_password(self, html):
        match = re.search(login_error[self.oj], html, re.M)
        return False if match else True

    def login(self):
        url = Login_url[self.oj]
        html = self.get_html(url, self.postdata)
        if not self.judge_password(html):
            logging.warning("Login ERRER!!! No Such User!!!")
            return False
            # sql = "UPDATE core_judge_account SET defunct = '1' WHERE id = '%s'" % (self.account_id)
            # Connect.query(sql)
        else:
            logging.info("OJ:" + self.oj + " USER: " + self.username + " Logined")
            return True

    def logined(self):
        url = oj_index[self.oj]
        html = self.get_html(url)
        match = re.search(not_login[self.oj], html, re.M)
        return False if match else True

    def add_path(self, path):
        if not os.path.exists(path):
            try:
                os.mkdir(path)
            except:
                logger.warning("img mkdir ERROR!!!")
                return

    def save_img(self, url, problem_id=''):
        filename = url.split('/')[-1]
        self.add_path(os.path.join(STATIC_PATH, 'uoload'))
        self.add_path(os.path.join(STATIC_PATH, 'uoload', self.oj))
        path = os.path.join(STATIC_PATH, 'upload', self.oj, str(problem_id))
        self.add_path(path)
        path = os.path.join(path, filename)
        if url[0:4] != 'http':
            url = url_index[self.oj] + url
        try:
            urllib.urlretrieve(url, path)
        except:
            logger.warning("Get Image ERROR!!!")
        else:
            logger.info("Download image <%s> over" % (filename))
