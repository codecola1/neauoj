__author__ = 'Code_Cola'

from access import Access

ac = Access(oj='hdu')
html = ac.get_html(url='http://acm.hdu.edu.cn/showproblem.php?pid=1002')
print html