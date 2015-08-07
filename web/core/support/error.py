#coding=utf-8
#!/usr/bin/python

__author__ = 'Code_Cola'

import datetime

logfile = open('../../web/log/error.txt', 'a')

Error = [
    'MySQL connect ERROR!!!',
    'MySQL query ERROR!!!',
    'Not Find User!!!',
    'Get HTML ERROR!!!',
    'Login ERROR!!!',
]

def error_write(error_index, other_error = ""):
    now = datetime.datetime.now().strftime("%Y-%m-%d %I:%M %p")
    error_str = now + ": " + Error[error_index] + ("\n" if not other_error else "\n" + "-"*20 + str(other_error))
    logfile.write(error_str + "\n")