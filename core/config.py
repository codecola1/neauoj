# coding=utf-8
__author__ = 'Code_Cola'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'neauoj',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': '',
        'POST': '3306'
    }
}

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

oj_index = {
    'hdu': 'http://acm.hdu.edu.cn',
    'poj': 'http://poj.org'
}

# Access
login_data = {
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

not_login = {
    'hdu': r'name=username',
    'poj': r'',
}

# vjudge
url_referer = {
    'hdu': 'http://acm.hdu.edu.cn/submit.php?pid=',
}  # referer

url_submit = {
    'hdu': 'http://acm.hdu.edu.cn/submit.php?action=submit',
}  # submit

url_status = {
    'hdu': ['http://acm.hdu.edu.cn/status.php', 'http://acm.hdu.edu.cn/status.php?first='],
}  # 查看status

url_ce = {
    'hdu': 'http://acm.hdu.edu.cn/viewerror.php?rid=',
}  # 查看CE详情

re_string = {
    'hdu': [r'22px>.*?%s', r'22px>(\w+)<', r'%s<.+?<font.*?>(.*?)</font>.*?(\d+)MS.*?(\d+)K', r'<pre>(.*?)</pre>'],
    # 各种匹配的正则
    # 0:缩小查找范围 以当前用户名为第一条记录
    # 1:确定所提交的RunID
    # 2:获取本RunID的提交结果
    # 3:抓取CE信息
}

post_data = {
    'hdu': {
        'check': '0',
        'problemid': '',
        'language': '',
        'usercode': '',
    }
}  # POST的相关数据

judge_listmap = {
    'hdu': ['problemid', 'language', 'usercode']
}  # POST数据项对应关系

language_map = {
    'hdu': {
        'c': '3',
        'c++': '2',
        'gcc': '1',
        'g++': '0',
        'java': '5'
    }
}  # 语言与对应需POST的数据
