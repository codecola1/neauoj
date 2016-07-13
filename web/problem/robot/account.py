__author__ = 'Code_Cola'

from access import *
from get_problem import *
from web.access_parameter import *
from status.models import Solve, ce_info
from users.models import submit_problem
import re
import MySQLdb
import socket
import HTMLParser


def test_account(oj, username, password):
    ac = Access(oj, username, password)
    return ac.logined()


def get_last_rid(oj, username):
    ac = Access(oj=oj)
    url = user_status[oj] % ('', username)
    html = ac.get_html(url=url)
    match = re.search(user_last_rid[oj], html, re.M)
    return match.group(1)


def updata_user(user):
    accounts = user.info.oj_account.all()
    k = 0
    for i in accounts:
        if not i.defunct:
            ret = get_last_rid(i.oj, i.username)
            if ret != i.last_rid and not i.is_using:
                k = 1
                client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
                client.connect("/tmp/neauoj.sock")
                client.send("1 " + str(user.id) + str(i.id))
                receive = client.recv(1024)
                client.close()
                # t = threading.Thread(target=updata_account(i, user, ret))
                # t.start()
    return k


def updata_account(account, user, last_rid):
    oj = account.oj
    username = account.username
    account.is_using = 1
    account.updating = 0
    account.save()
    ac = Access(oj, username, account.password)
    if ac.logined():
        status = []
        url = user_status[oj] % ('', username)
        html = ac.get_html(url=url)
        match = re.compile(get_status[oj], re.M | re.I | re.S)
        result = match.findall(html)
        i = 0
        while result[i][0] != account.last_rid:
            try:
                p = Problem.objects.get(oj=oj, problem_id=result[i][3])
            except:
                test = Down_problem(oj, result[i][3])
                if test.right:
                    test.get_info()
                    test.get_img()
                    p = Problem.objects.get(oj=oj, problem_id=result[i][3])
                else:
                    return
            status.append(
                [result[i][2], p.id, result[i][4], result[i][5], result[i][6], result[i][7], result[i][1],
                 result[i][0]])
            i += 1
            if i == len(result):
                url = user_status[oj] % (int(result[i - 1][0]) - 1, username)
                html = ac.get_html(url=url)
                result = match.findall(html)
                if len(result) == 0:
                    break
                i = 0
        l = len(status)
        j = 1
        for i in status:
            p = Problem.objects.get(id=i[1])
            try:
                code = get_code(ac.get_html(url=get_code_url[oj] % i[7]), oj)
            except:
                code = ''
            s = Solve(status=i[0], problem=p, use_time=i[2], use_memory=i[3], length=i[4], language=i[5], code=code,
                      user=user)
            s.save()
            s.submit_time = i[6]
            s.save()
            if i[0] == 'Compilation Error':
                try:
                    ce_info_t = get_ce_info(ac.get_html(url=get_ce_url[oj] % i[7]), oj)
                except:
                    ce_info_t = ''
                c = ce_info(info=ce_info_t, solve=s)
                c.save()
            try:
                sp = submit_problem.objects.get(problem=p, user=user)
            except:
                sp = submit_problem(ac=1 if i[0] == 'Accepted' else 0, problem=p, user=user)
            else:
                if not sp.ac and i[0] == 'Accepted':
                    sp.ac = 1
            sp.save()
            account.updating = str(int(j / float(l) * 100))
            account.save()
            j += 1
        account.last_rid = last_rid
        account.is_using = 0
        account.save()


def get_code(html, oj):
    match = re.search(get_code_re[oj], html, re.M | re.DOTALL)
    try:
        code = unicode(match.group(1), "utf-8")
    except:
        code = ''
    html_parser = HTMLParser.HTMLParser()
    return html_parser.unescape(code)


def get_ce_info(html, oj):
    t = re.search(get_ce_re[oj], html, re.M | re.I | re.S)
    try:
        string = t.group(1)
    except:
        string = ''
    return string
