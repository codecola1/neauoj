__author__ = 'Code_Cola'

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

url_index = {
    'hdu': 'http://acm.hdu.edu.cn',
    'poj': 'http://poj.org'
}

oj_index = {
    'hdu': 'http://acm.hdu.edu.cn',
    'poj': 'http://poj.org'
}

Listmap = {
    'hdu': ['username', 'userpass'],
    'poj': ['user_id1', 'password1']
}

decode = {
    'hdu': True,
    'poj': False
}

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

login_error = {
    'hdu': r'<input name=username',
    'poj': r'User\sID',
}

not_login = {
    'hdu': r'name=username',
    'poj': r'',
}

user_status = {
    'hdu': r'http://acm.hdu.edu.cn/status.php?first=%s&user=%s',
}

user_last_rid = {
    'hdu': r'</form></td></tr><tr align=center ><td height=22px>([0-9]*)</td><td>',
}

get_status = {
    'hdu': r'<td height=22px>([0-9]*)</td><td>(.{19})</td>.*?<font.+?>(.+?)</font>.+?pid=([0-9]*).+?<td>([0-9]*)MS.+?<td>([0-9]*)K.+?>([0-9]*).B</td><td>(.*?)</td><td class',
}

get_code_url = {
    'hdu': 'http://acm.hdu.edu.cn/viewcode.php?rid=%s',
}

get_code_re = {
    'hdu': r'none;text-align:left;">(.*)</textarea>',
}

get_ce_url = {
    'hdu': 'http://acm.hdu.edu.cn/viewerror.php?rid=%s',
}

get_ce_re = {
    'hdu': r'<pre>(.*?)</pre>',
}
