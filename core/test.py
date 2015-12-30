# coding=utf-8
__author__ = 'Code_Cola'

import access, re

ac = access.Access(oj='hdu')
url = 'http://acm.hdu.edu.cn/showproblem.php?pid='
# pid = 1002
for pid in range(1000, 2000):
    html = ac.get_html(url=url + str(pid))
    print pid
