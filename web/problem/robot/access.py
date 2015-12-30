# coding=utf-8
#!/usr/bin/python
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
    def __init__(self, oj=''):
        self.cookie = cookielib.CookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookie))
        self.safe = True
        self.oj = oj
        self.header = Headers[self.oj]

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
            logger.warning("Get HTML ERROR!!!" + e.reason)
            self.safe = False
            return ''
        else:
            logger.info("get_html:" + url)
            return s

    def save_img(self, url, problem_id=''):
        filename = url.split('/')[-1]
        path = os.path.join(STATIC_PATH, 'upload', self.oj, str(problem_id))
        if not os.path.exists(path):
            try:
                os.mkdir(path)
            except:
                logger.warning("img mkdir ERROR!!!")
                return
        path = os.path.join(path, filename)
        if url[0:4] != 'http':
            url = url_index[self.oj] + url
        try:
            urllib.urlretrieve(url, path)
        except:
            logger.warning("Get Image ERROR!!!")
        else:
            logger.info("Download image <%s> over" % (filename))