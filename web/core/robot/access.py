#coding=utf-8
#!/usr/bin/python
__author__ = 'Code_Cola'

import urllib
import urllib2
import cookielib
import re

from core.support.error import error_write
from core.support.mysql_join import Connect

Headers = {
    'hdu': {
        'Host': 'acm.hdu.edu.cn',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Referer': 'http://acm.hdu.edu.cn/',
        'Connection': 'keep-alive'
    },
    'poj': {
        'Host': 'poj.org',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Referer': 'http://poj.org/',
        'Connection': 'keep-alive'
    }
}

Data = {
    'hdu': {
        'username': '',
        'userpass': '',
        'login': 'Sign In'
    },
    'poj': {
        'user_id1': '',
        'password1': '',
        'B1': 'login',
        'url': '/'
    }
}

Login_url = {
    'hdu': 'http://acm.hdu.edu.cn/userloginex.php?action=login',
    'poj': 'http://poj.org/login'
}

Listmap = {
    'hdu': ['username', 'userpass'],
    'poj': ['user_id1', 'password1']
}

decode = {
    'hdu': True,
    'poj': False
}

class Access:
    def __init__(self, account_id='', oj=''):
        self.accunt_id = account_id
        self.cookie = cookielib.CookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookie))
        self.safe = True
        if account_id != '':
            self.get_user()
        else:
            self.oj = oj
            self.header = Headers[self.oj]

    def get_user(self):
        sql = "SELECT username, password, oj FROM users_account WHERE id = '%s'" % (self.accunt_id)
        results = Connect.query(sql)
        if results:
            self.username = str(results[0][0])
            self.password = str(results[0][1])
            self.oj = str(results[0][2])
        else:
            error_write(2)
            self.safe = False
            return
        self.postdata = Data[self.oj]
        self.postdata[Listmap[self.oj][0]] = self.username
        self.postdata[Listmap[self.oj][1]] = self.password
        self.oj = Headers[self.oj]

    def get_html(self, url, postdata = {}):
        if not self.safe:
            return ''
        req = urllib2.Request(url = url, headers = self.header, data = None if not len(postdata) else urllib.urlencode(postdata))
        try:
            s = self.opener.open(req).read()
            if decode[self.oj]:
                s = s.decode('gbk').encode('utf8')
        except urllib2.URLError, e:
            error_write(3, other_error=e.reason)
            self.safe = False
            return ''
        else:
            return s

    def login(self):
        url = Login_url[self.oj]
        html = self.get_html(url, self.postdata)
        if self.safe:
            if self.oj == 'hdu':
                def judge_password(html):
                    match = re.search(r'No\ssuch\suser\sor\swrong\spassword',html,re.M)
                    return False if match else True
            elif self.oj == 'poj':
                def judge_password(html):
                    match = re.search(r'User\sID',html,re.M);
                    return False if match else True
            if not judge_password(html):
                self.safe = False
                error_write(4)
                sql = "UPDATE users_account SET defunct = '1' WHERE account_id = '%s'" % (self.account_id)
                Connect.query(sql)