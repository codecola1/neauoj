# coding=utf-8
# !/usr/bin/python

__author__ = 'Code_Cola'

import MySQLdb
from config import DATABASES
from log_judge import Log

host = 'localhost'
username = DATABASES['default']['USER']
password = DATABASES['default']['PASSWORD']
database = DATABASES['default']['NAME']
logging = Log()

class MySQLQueryError(IndexError):
    pass

class MySQL:
    def __init__(self):
        try:
            self.db = MySQLdb.connect(host, username, password, database, charset="utf8")
        except:
            logging.warning('MySQL connect ERROR!!!')
            self.db = None
        else:
            self.cursor = self.db.cursor()

    def update(self, sql):
        try:
            self.cursor.execute(sql)
        except:
            logging.warning('MySQL update ERROR!!! SQL: %s' % sql)
        else:
            self.db.commit()

    def query(self, sql):
        try:
            self.cursor.execute(sql)
        except:
            logging.warning('MySQL query ERROR!!! SQL: %s' % sql)
            return ''
        else:
            return self.cursor.fetchall()

    def get_id(self):
        try:
            id = self.cursor.lastrowid
        except:
            logging.warning('MySQL get_id ERROR!!!')
            return ''
        else:
            return id
