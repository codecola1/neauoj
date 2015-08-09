# __author__ = 'Code_Cola'
#
# import re
#
# from access import Access
# from HTMLParser import HTMLParser
#
# img = []
#
# class MyHTMLParser(HTMLParser):
#     def handle_starttag(self, tag, attrs):
#         if tag == 'img' and len(attrs) == 1:
#             img.append(attrs[0][1])
#
# ac = Access(oj='hdu')
# html = ac.get_html(url='http://acm.hdu.edu.cn/showproblem.php?pid=2383')
# # ac = Access(oj='poj')
# # html = ac.get_html(url='http://poj.org/problem?id=1027')
# parser = MyHTMLParser()
# parser.feed(html)
# match = re.search(r'<h1.*?>(.+?)</h1>', html, re.M | re.I | re.DOTALL)
# Title = match.group(1)
# match = re.search(r'Time Limit: (\d*?)/(\d*?) MS', html, re.M | re.I | re.DOTALL)
# Time_Limit_C = match.group(2)
# Time_Limit_Java = match.group(1)
# match = re.search(r'Memory Limit: (\d*?)/(\d*?) K', html, re.M | re.I | re.DOTALL)
# Memory_Limit_C = match.group(2)
# Memory_Limit_Java = match.group(1)
# match = re.search(r'Desc.*?t>(.+?)</div>', html, re.M | re.I | re.DOTALL)
# Description = match.group(1)
# match = re.search(r'[^ ]Input<.*?t>(.+?)</div>', html, re.M | re.I | re.DOTALL)
# Input = match.group(1)
# match = re.search(r'[^ ]Output<.*?t>(.+?)</div>', html, re.M | re.I | re.DOTALL)
# Output = match.group(1)
# match = re.search(r' Input<.*?style.*?>(.+?)</div>', html, re.M | re.I | re.DOTALL)
# Sinput = match.group(1)
# match = re.search(r' Output<.*?style.*?>(.+?)</?div', html, re.M | re.I | re.DOTALL)
# Soutput = match.group(1)
# match = re.search(r'(?:Hint.*?Hint.*?</div|Hint</i).*?</(?:i>|div>)(.+?)</div>', html, re.M | re.I | re.DOTALL)
# if match:
#     Soutput = Soutput[0:-3]
#     Hint = match.group(1)[2:]
# else:
#     Hint = ""
# match = re.search(r'Author</d.*?t>(.+?)</div>', html, re.M | re.I | re.DOTALL)
# if match:
#     Author = match.group(1)
# else:
#     Author = ""
#
# print '\n'.join([Title, "Time C: " + Time_Limit_C, "Time Java: " + Time_Limit_Java, "Memory C: " + Memory_Limit_C, "Memory Java: " + Memory_Limit_Java, Description, Input, Output, Sinput, Soutput, Hint, Author])

from problem.robot.get_problem import Problem
p = Problem('hdu', '2353')
if p.right:
    p.get_img()