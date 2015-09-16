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

Data = {
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

url_index = {
    'hdu': 'http://acm.hdu.edu.cn',
    'poj': 'http://poj.org'
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