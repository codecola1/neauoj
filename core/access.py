# coding=utf-8
#!/usr/bin/python
__author__ = 'Code_Cola'

import urllib
import urllib2
import cookielib
import re
import os

from support.log_judge import Log
from settings import *

logging = Log()


class Access:
    def __init__(self, oj='', username='', password=''):
        self.cookie = cookielib.CookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookie))
        self.safe = True
        self.oj = oj
        self.header = Headers[self.oj]
        if username:
            self.username = username
            self.postdata = Data[self.oj]
            self.postdata[Listmap[self.oj][0]] = username
            self.postdata[Listmap[self.oj][1]] = password
            self.login()

    def get_html(self, url, postdata={}, referer=''):
        if not self.safe:
            return ''
        header = self.header
        if referer:
            header['Referer'] = referer
        req = urllib2.Request(url=url, headers=header,
                              data=None if not len(postdata) else urllib.urlencode(postdata))
        try:
            s = self.opener.open(req).read()
            if decode[self.oj]:
                s = s.decode('gbk').encode('utf8')
        except urllib2.URLError, e:
            logging.warning("Get HTML ERROR!!!" + e.reason)
            self.safe = False
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
        if self.safe:
            if not self.judge_password(html):
                self.safe = False
                logging.warning("Login ERRER!!! No Such User!!!")
                # sql = "UPDATE core_judge_account SET defunct = '1' WHERE id = '%s'" % (self.account_id)
                # Connect.query(sql)
            else:
                logging.info("OJ:" + self.oj + " USER: " + self.username + " Logined")
                return True
        logging.warning("Login ERROR!!!")
        return False
