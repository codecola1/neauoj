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


class MySQLConnectError(Exception):
    pass


class MySQLQueryError(Exception):
    pass


class MySQL:
    def __init__(self):
        try:
            self.db = MySQLdb.connect(host, username, password, database, charset="utf8")
        except MySQLdb.Error, e:
            try:
                error_message = "Error %d:%s" % (e.args[0], e.args[1])
            except IndexError:
                error_message = "MySQL Error:%s" % str(e)
            logging.warning(error_message)
            raise
        else:
            self.cursor = self.db.cursor()

    def update(self, sql):
        try:
            self.cursor.execute(sql)
        except MySQLdb.Error, e:
            logging.warning('MySQL update ERROR!!! Error: %s & SQL: %s' % (str(e), sql))
            return False
        else:
            self.db.commit()
            return True

    def query(self, sql):
        try:
            self.cursor.execute(sql)
        except MySQLdb.Error, e:
            logging.warning('MySQL query ERROR!!! Error: %s & SQL: %s' % (str(e), sql))
            raise MySQLQueryError
        else:
            return self.cursor.fetchall()

    def get_id(self):
        try:
            id = self.cursor.lastrowid
        except MySQLdb.Error, e:
            logging.warning('MySQL get_id ERROR!!! Error: %s' % str(e))
            raise MySQLQueryError
        else:
            return id
