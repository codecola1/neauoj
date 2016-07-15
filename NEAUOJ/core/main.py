# -*- coding:utf-8 -*-
# !/usr/bin/python

__author__ = 'Code_Cola'

import sys
from bin.log import Log
from bin.problem import Problem
from db.mysql import MySQL
from core.connect import Connect
from core.judge_server import JudgeServer
from core.problem_server import ProblemServer

logging = Log()


class BuildQueueError(Exception):
    def __init__(self, arg):
        self.args = arg


class Main:
    """
        Web端通信格式：
            0: 判题模块
                参数：[操作数 (任务消息)]
            1：Down题模块
                参数：OJ缩写 Problem_id pid
            2: 获取题目信息
                参数：OJ缩写 Problem_id
            3: 更新模块
                参数：用户id
    """

    def __init__(self):
        self.mysql = MySQL()
        self.Judging = JudgeServer()
        self.Download = ProblemServer()
        self.Judging.setDaemon(True)
        self.Download.setDaemon(True)

    def __del__(self):
        self.Judging.judge_stop()

    def start(self):
        self.Judging.start()
        self.Download.start()
        connect = Connect()
        while True:
            message = connect.get_message()
            try:
                if message[0] == '0':
                    JudgeServer.judge_task.put(message[1:])
                elif message[0] == '1':
                    ProblemServer.problem_task.put(message[1:])
                elif message[0] == '2':
                    try:
                        p = Problem(message[1], message[2], 0)
                    except IndexError:
                        pass
                    else:
                        title = p.get_title()
                        connect.receive_message("%s" % title)
                else:
                    raise IndexError
            except IndexError:
                logging.error("Error message!!! message: " + ' '.join(message))
            else:
                connect.receive_message()
                connect.close_connect()


if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf8')
    try:
        main = Main()
        main.start()
    except KeyboardInterrupt:
        pass
