# coding=utf-8
#!/usr/bin/python
__author__ = 'Code_Cola'

import urllib
import urllib2
import cookielib
import re
import os

from core.support.mysql_join import Connect
from web.settings import STATIC_PATH
from core.support.log_main import Log

logging = Log()

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

url_index = {
    'hdu': 'http://acm.hdu.edu.cn',
    'poj': 'http://poj.org'
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

login_error = {
    'hdu': r'No\ssuch\suser\sor\swrong\spassword',
    'poj': r'User\sID',
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
            logging.warning("get_user MySQL query ERROR!!!")
            self.safe = False
            return
        self.postdata = Data[self.oj]
        self.postdata[Listmap[self.oj][0]] = self.username
        self.postdata[Listmap[self.oj][1]] = self.password
        self.oj = Headers[self.oj]

    def get_html(self, url, postdata={}):
        if not self.safe:
            return ''
        req = urllib2.Request(url=url, headers=self.header,
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
                sql = "UPDATE users_account SET defunct = '1' WHERE account_id = '%s'" % (self.account_id)
                Connect.query(sql)
            else:
                logging.info("OJ:" + self.oj + " USER:" + self.username + "Logined")
                return True
        logging.warning("Login ERROR!!!")
        return False

    def save_img(self, url, problem_id=''):
        filename = url.split('/')[-1]
        path = os.path.join(STATIC_PATH, 'upload', self.oj, str(problem_id))
        if not os.path.exists(path):
            try:
                os.mkdir(path)
            except:
                logging.warning("img mkdir ERROR!!!")
                return
        path = os.path.join(path, filename)
        if url[0:4] != 'http':
            url = url_index[self.oj] + ('' if url[0] == '/' else '/') + url
        try:
            # conn = urllib.urlopen(url)
            # f = open(path,'wb')
            # f.write(conn.read())
            # f.close()
            urllib.urlretrieve(url, path)
        except:
            logging.warning("Get Image ERROR!!!")
        else:
            logging.info("Download image <%s> over" % (filename))