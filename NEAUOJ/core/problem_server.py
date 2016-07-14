# -*- coding:utf-8 -*-
# !/usr/bin/python

__author__ = 'Code_Cola'

from Queue import Queue
import threading
from bin.log import Log
from bin.problem import Problem
from bin.access import ProblemAccess
from db.mysql import MySQL, MySQLQueryError
from conf.global_config import *

logging = Log()


class ProblemServer(threading.Thread):
    """
        Problem服务
        任务获取格式：

            (oj, problem_id, pid)    Down题请求
    """
    problem_task = None
    semaphore = threading.Semaphore(Task_Limit)

    def __init__(self):
        super(ProblemServer, self).__init__()
        self.mysql = MySQL()
        ProblemServer.problem_task = Queue(Task_Limit)

    def run(self):
        while True:
            task = ProblemServer.problem_task.get()
            try:
                oj = task[0]
                problem_id = task[1]
                pid = task[2]
            except IndexError:
                logging.error("Error message!!! message: " + ' '.join(message))
            else:
                dp = DownloadProblem(oj, problem_id, pid)
                dp.start()


class DownloadProblem(threading.Thread):
    def __init__(self, oj, problem_id, pid):
        super(DownloadProblem, self).__init__()
        self.oj = oj
        self.problem_id = problem_id
        self.pid = pid

    def run(self):
        if ProblemServer.semaphore.acquire():
            p = Problem(self.oj, self.problem_id, self.pid)
            p.run()
            ProblemServer.semaphore.release()
