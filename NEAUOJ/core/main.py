# -*- coding:utf-8 -*-
# !/usr/bin/python

__author__ = 'Code_Cola'

import sys
from bin.log import logging
from bin.problem import Problem
from db.mysql import MySQL
from core.connect import Connect
from core.judge_server import JudgeServer
from core.problem_server import ProblemServer
from core.contest import *


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
            3: 测试OJ账号
                参数：OJ缩写 username password
            4: 更新模块
                参数：用户id
            5: 测试Contest_ID
                参数：OJ缩写 Contest_ID
            6: 克隆比赛
                参数：OJ缩写 Contest_ID
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
                        connect.receive_message("")
                    else:
                        title = p.get_title()
                        connect.receive_message("%s" % title)
                elif message[0] == '3':
                    connect.receive_message("0")
                elif message[0] == '4':
                    pass
                elif message[0] == '5':
                    oj = message[1]
                    username = message[2]
                    password = message[3]
                    cid = int(message[4])
                    c = Contest(oj, username, password, cid, -1)
                    connect.receive_message("%d" % c.get_problem_number())
                elif message[0] == '6':
                    oj = message[1]
                    username = message[2]
                    password = message[3]
                    cid = int(message[4])
                    contest_id = int(message[5])
                    c = Contest(oj, username, password, cid, contest_id)
                    c.start()
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
