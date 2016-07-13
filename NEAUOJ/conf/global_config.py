# -*- coding:utf-8 -*-
# !/usr/bin/python

__author__ = 'Code_Cola'

import os
from local_config import *

OJ_NAME = 'neauoj'

DATABASES = {
    'default': {
        'NAME': 'neauoj',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': 'localhost',
        'POST': '3306'
    }
}

Local_PATH = '/'.join(os.getcwd().split('/')[0:-1])
Daemon_PATH = "/tmp/" + OJ_NAME + ".pid"
Socket_PATH = "/tmp/" + OJ_NAME + ".sock"
Log_PATH = Local_PATH + "/log/" + OJ_NAME + ".log"
Work_PATH = Local_PATH + "/work/run"
Data_PATH = Local_PATH + "/data/"

Task_Limit = 100
Local_Judge_Limit = 5

Language_Map = {
    'c': ['0', 'c'],
    'C': ['0', 'c'],
    'c++': ['1', 'cpp'],
    'C++': ['1', 'cpp'],
    'g++': ['2', 'cc'],
    'G++': ['2', 'cc'],
    'java': ['3', 'java'],
    'Java': ['3', 'java'],
}

Judge_Map = ['Accepted', 'Wrong Answer', 'Presentation Error', 'Compilation Error', 'Time Limit Exceeded',
             'Memory Limit Exceeded', 'Runtime Error']

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

OJ_Index = {
    'hdu': 'http://acm.hdu.edu.cn',
    'poj': 'http://poj.org'
}

OJ_Decode = {
    'hdu': True,
    'poj': False
}

Login_URL = {
    'hdu': 'http://acm.hdu.edu.cn/userloginex.php?action=login',
    'poj': 'http://poj.org/login'
}

Login_Data = {
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

Login_Data_List = {
    'hdu': ['username', 'userpass'],
    'poj': ['user_id1', 'password1']
}

Login_ERROR = {
    'hdu': r'No\ssuch\suser\sor\swrong\spassword',
    'poj': r'User\sID',
}

NOT_Login = {
    'hdu': r'name=username',
    'poj': r'User ID:',
}

RE_Last_Submit = {
    'hdu': r'22px>(\w+)<',
    'poj': r'<tr align=center><td>(\w+)<'
}

URL_Last_Submit = {
    'hdu': 'http://acm.hdu.edu.cn/status.php?user=',
    'poj': 'http://poj.org/status?user_id='
}

URL_Referer = {
    'hdu': 'http://acm.hdu.edu.cn/submit.php?pid=',
    'poj': 'http://poj.org/submit'
}  # referer

URL_Submit = {
    'hdu': 'http://acm.hdu.edu.cn/submit.php?action=submit',
    'poj': 'http://poj.org/submit'
}  # submit

URL_Status = {
    'hdu': 'http://acm.hdu.edu.cn/status.php?user=',
    'poj': 'http://poj.org/status?user_id='
}  # 查看status

URL_CE = {
    'hdu': 'http://acm.hdu.edu.cn/viewerror.php?rid=',
    'poj': 'http://poj.org/showcompileinfo?solution_id='
}  # 查看CE详情

RE_Judge_Status = {
    'hdu': r'%s<.+?<font.*?>(.*?)</font>.*?(\d+)MS.*?(\d+)K',
    'poj': r'%s<.+?<font.*?>(.*?)</font>.*?(\d+)MS.*?(\d+)K',
}

RE_Get_CE = {
    'hdu': r'<pre>(.*?)</pre>',
    'poj': r'<pre>(.*?)</pre>'
}

Submit_POST_Data = {
    'hdu': {
        'check': '0',
        'problemid': '',
        'language': '',
        'usercode': '',
    },
    'poj': {
        'problem_id': '',
        'language': '',
        'source': '',
        'submit': 'submit',
        'encoded': '1'
    }
}  # POST的相关数据

Submit_POST_Data_List = {
    'hdu': ['problemid', 'language', 'usercode'],
    'poj': ['problem_id', 'language', 'source']
}  # POST数据项对应关系

VJ_Language_Map = {
    'hdu': {
        'c': '3',
        'C': '3',
        'c++': '2',
        'C++': '2',
        'gcc': '1',
        'GCC': '1',
        'g++': '0',
        'G++': '0',
        'java': '5',
        'Java': '5'
    },
    'poj': {
        'c': '5',
        'C': '5',
        'c++': '4',
        'C++': '4',
        'gcc': '1',
        'GCC': '1',
        'g++': '0',
        'G++': '0',
        'java': '2',
        'Java': '2'
    }
}  # 语言与对应需POST的数据
