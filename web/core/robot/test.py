__author__ = 'Code_Cola'

from access import Access
from HTMLParser import HTMLParser

img = []

class MyHTMLParser(HTMLParser):

    def handle_starttag(self, tag, attrs):
        if tag == 'img' and len(attrs) == 1:
            img.append(attrs[0][1])

ac = Access(oj='hdu')
html = ac.get_html(url='http://acm.hdu.edu.cn/showproblem.php?pid=1022')
# ac = Access(oj='poj')
# html = ac.get_html(url='http://poj.org/problem?id=1027')
parser = MyHTMLParser()
parser.feed(html)
for url in img:
    ac.save_img(url)