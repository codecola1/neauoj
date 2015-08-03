#coding=utf-8
#!/usr/bin/python

__author__ = 'Code_Cola'

import MySQLdb
from web.settings import DATABASES
from error import Error_log

host = 'localhost'
username = DATABASES['default']['USER']
password = DATABASES['default']['PASSWORD']
database = DATABASES['default']['NAME']


class Connect:
    def __init__(self):
        try:
            db = MySQLdb.connect(host, username, password, database, charset="utf8")
        except:
            Error_log.write(0)
        self.cursor = db.cursor()
    def query(self, sql):
        try:
            self.cursor.execute(sql)
        except:
            Error_log.write(1)
            return ''
        else:
            return self.cursor.fetchall()