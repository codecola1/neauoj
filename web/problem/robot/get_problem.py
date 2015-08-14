__author__ = 'Code_Cola'

import re
import urllib
from HTMLParser import HTMLParser
from core.robot.access import Access
from problem.models import Problem

url = {
    'hdu': 'http://acm.hdu.edu.cn/showproblem.php?pid=',
    'poj': 'http://poj.org/problem?id=',
}

r = {
    'hdu': [
        r'(?:No such problem|Invalid Parameter)(.*?)</div>',
        r'<h1.*?>(.+?)</h1>',
        r'Time Limit: (\d*?)/(\d*?) MS',
        r'Memory Limit: (\d*?)/(\d*?) K',
        r'Desc.*?t>(.+?)</div>',
        r'[^ ]Input<.*?t>(.+?)</div>',
        r'[^ ]Output<.*?t>(.+?)</div>',
        r' Input<.*?style.*?>(.+?)</div>',
        r' Output<.*?style.*?>(.+?)</?div',
        r'(?:Hint.*?Hint.*?</div|Hint</i).*?</(?:i>|div>)(.+?)</div>',
        r'>Author<.*?t>(.*?)</div>',
    ],
    'poj': [
        r'Error Occurred(.*?)>',
        r'<div class="ptt".*?>(.*?)</div>',
        r'Time Limit:</b> (.*?)MS',
        r'Memory Limit:</b> (.*?)K',
        r'Desc.*?">(.*?)</div>',
        r'>Input.*?">(.*?)</div>',
        r'>Output.*?">(.*?)</div>',
        r' Input<.*?">(.*?)</pre>',
        r' Output<.*?">(.*?)</pre>',
        r'Hint(.*?)</div>',
        r'Source.*?<a.*?">(.*?)</',
    ]
}

replace = {
    'hdu': r'/data/images/',
    'poj': r'images([/\d]*)/'
}

img = []


class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        if tag == 'img' and len(attrs) == 1:
            img.append(attrs[0][1])


def use_re(ri, data, oj, n=1):
    match = re.search(r[oj][ri], data, re.M | re.I | re.DOTALL)
    if match:
        if n == 1:
            return match.group(1)
        ret = []
        for i in range(1, n + 1):
            ret.append(match.group(i))
        return ret
    else:
        return "" * n


class Down_problem:
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
            i = i.replace('../', '')
            self.ac.save_img(i if i[0] == '/' else '/' + i, self.pid)

    def get_info(self):
        self.Title = use_re(1, self.html, self.ojname)
        if self.ojname == 'poj':
            self.Time_Limit_C = use_re(2,self.html,self.ojname)
            self.Memory_Limit_C = use_re(3,self.html,self.ojname)
            self.Time_Limit_Java = 2 * self.Time_Limit_C
            self.Memory_Limit_Java = self.Memory_Limit_C
        else:
            self.Time_Limit_Java, self.Time_Limit_C = use_re(2, self.html, self.ojname, 2)
            self.Memory_Limit_Java, self.Memory_Limit_C = use_re(3, self.html, self.ojname, 2)
        path = '/upload/' + self.ojname + "/" + str(self.pid) + "/"
        self.Description = use_re(4, self.html, self.ojname)#.replace(replace[self.ojname], ("/" + path) if self.ojname == 'poj' else path)
        self.Input = use_re(5, self.html, self.ojname)#.replace(replace[self.ojname], ("/" + path) if self.ojname == 'poj' else path)
        self.Output = use_re(6, self.html, self.ojname)#.replace(replace[self.ojname], ("/" + path) if self.ojname == 'poj' else path)
        self.Description = re.sub(replace[self.ojname], path, self.Description)
        self.Input = re.sub(replace[self.ojname], path, self.Input)
        self.Output = re.sub(replace[self.ojname], path, self.Output)
        self.Sinput = use_re(7, self.html, self.ojname).replace('\n', '<br>')
        self.Soutput = use_re(8, self.html, self.ojname).replace('\n', '<br>')
        self.Hint = use_re(9, self.html, self.ojname)
        if self.Hint:
            self.Soutput = self.Soutput[0:-6]
        self.Source = use_re(10, self.html, self.ojname)
        p = Problem(
            title=self.Title,
            time_limit_c=self.Time_Limit_C,
            memory_limit_c=self.Memory_Limit_C,
            time_limit_java=self.Time_Limit_Java,
            memory_limit_java=self.Memory_Limit_Java,
            description=self.Description,
            input=self.Input,
            output=self.Output,
            sample_input=self.Sinput,
            sample_output=self.Soutput,
            hint=self.Hint,
            source=self.Source,
            oj=self.ojname,
            problem_id=self.pid,
            judge_type=1,
        )
        # p.save()