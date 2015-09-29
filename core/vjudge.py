__author__ = 'Code_Cola'

from access import Access
from support.mysql_join import Connect
from time import sleep
import re

url_index = {
    'hdu': 'http://acm.hdu.edu.cn/submit.php?pid=',
}

url_submit = {
    'hdu': 'http://acm.hdu.edu.cn/submit.php?action=submit',
}

url_status = {
    'hdu': ['http://acm.hdu.edu.cn/status.php', 'http://acm.hdu.edu.cn/status.php?first='],
}

url_ce = {
    'hdu': 'http://acm.hdu.edu.cn/viewerror.php?rid=',
}

re_string = {
    'hdu': [r'22px>.*?%s', r'22px>(\w+)<', r'%s<.+?<font.*?>(.*?)</font>.*?(\d+)MS.*?(\d+)K', r'<pre>(.*?)</pre>'],
}

post_data = {
    'hdu': {
        'check': '0',
        'problemid': '',
        'language': '',
        'usercode': '',
    }
}

Listmap = {
    'hdu': ['problemid', 'language', 'usercode']
}

language_map = {
    'hdu': {
        'c': '3',
        'c++': '2',
        'gcc': '1',
        'g++': '0',
        'java': '5'
    }
}


class Vjudge:
    def __init__(self, sid, username, password):
        self.mysql = Connect()
        self.sid = sid
        self.get_info(sid)
        self.username = username
        self.ac = Access(self.oj, username, password)
        self.ce_info = ''

    def get_info(self, sid):
        result = self.mysql.query("SELECT problem_id, language, code FROM status_solve WHERE id = '%s'" % sid)
        self.language = result[0][1]
        self.code = result[0][2]
        result = self.mysql.query("SELECT oj, problem_id FROM problem_problem WHERE id = '%s'" % result[0][0])
        self.oj = result[0][0]
        self.pid = result[0][1]

    def submit(self):
        url = url_submit[self.oj]
        referer = url_index[self.oj] + self.pid
        postdata = post_data[self.oj]
        postdata[Listmap[self.oj][0]] = self.pid
        postdata[Listmap[self.oj][1]] = language_map[self.oj][self.language]
        postdata[Listmap[self.oj][2]] = self.code
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
            sql = "INSERT INTO status_ce_info (info, solve_id) VALUES('%s', '%s')" % (self.ce_info, self.sid)
            self.mysql.update(sql)
        if o[0] == 'Accepted':
            self.mysql.update("UPDATE problem_problem SET solved = solved + '1' WHERE id = '%s'" % self.sid)