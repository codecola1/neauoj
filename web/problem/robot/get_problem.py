__author__ = 'Code_Cola'

import re
import urllib
from HTMLParser import HTMLParser
from core.robot.access import Access

url = {
    'hdu': 'http://acm.hdu.edu.cn/showproblem.php?pid='
}

r = {
    'hdu': [
        r'No such problem',
        r'<h1.*?>(.+?)</h1>',
        r'Time Limit: (\d*?)/(\d*?) MS',
        r'Memory Limit: (\d*?)/(\d*?) K',
        r'Desc.*?t>(.+?)</div>',
        r'[^ ]Input<.*?t>(.+?)</div>',
        r'[^ ]Output<.*?t>(.+?)</div>',
        r' Input<.*?style.*?>(.+?)</div>',
        r' Output<.*?style.*?>(.+?)</?div',
        r'(?:Hint.*?Hint.*?</div|Hint</i).*?</(?:i>|div>)(.+?)</div>',
    ]
}

img = []


class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        if tag == 'img' and len(attrs) == 1:
            img.append(attrs[0][1])

def use_re(ri, data, oj, n=1):
    match = re.search(r[oj][ri], data, re.M | re.I | re.DOTALL)
    if match:
        ret = []
        for i in range(1, n + 1):
            ret.append(match.group(i))
        return ret
    else:
        return "" * n


class Problem:
    def __init__(self, ojname, pid):
        self.ojname = ojname
        self.pid = pid
        self.right = False
        self.ac = Access(oj=ojname)
        global img
        img = []
        self.html = self.ac.get_html(url=url[self.ojname] + str(self.pid))
        if not use_re(0, self.html, self.ojname):
            self.right = True

    def get_img(self):
        parser = MyHTMLParser()
        parser.feed(self.html)
        for i in img:
            self.ac.save_img(i, self.pid)