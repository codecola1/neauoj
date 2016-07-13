# -*- coding:utf-8 -*-
# !/usr/bin/python

__author__ = 'Code_Cola'

import sys
from bin.log import Log
from db.mysql import MySQL
from core.connect import Connect
from core.judge_server import JudgeServer


class BuildQueueError(Exception):
    def __init__(self, arg):
        self.args = arg


class Main:
    """
        Web端通信格式：
            0: 判题模块
                参数：[操作数 (任务消息)]
            1：更新模块
                参数：用户id
            2: Down题模块
                参数：OJ缩写 Problem_id
    """

    def __init__(self):
        self.mysql = MySQL()
        self.Judging = JudgeServer()
        self.Judging.setDaemon(True)

    def __del__(self):
        self.Judging.judge_stop()

    def start(self):
        self.Judging.start()
        connect = Connect()
        while True:
            message = connect.get_message()
            try:
                if message[0] == '0':
                    JudgeServer.judge_task.put(message[1:])
                elif message[0] == '1':
                    pass
                elif message[0] == '2':
                    pass
                else:
                    raise IndexError
            except IndexError:
                logging.error("Error message!!! message: " + ' '.join(message))
            else:
                connect.receive_message()


if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf8')
    try:
        main = Main()
        main.start()
    except KeyboardInterrupt:
        pass
