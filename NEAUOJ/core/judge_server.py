# -*- coding:utf-8 -*-
# !/usr/bin/python

__author__ = 'Code_Cola'

from Queue import Queue
import threading
from bin.log import Log
from bin.judge import VirtualJudge
from bin.access import JudgeAccess
from db.mysql import MySQL, MySQLQueryError
from conf.global_config import *
from vjudge import Vjudge


class JudgeServer(threading.Thread):
    """
        Judge服务
        任务获取格式：
            [operator (task)]
            [操作数 (任务消息)]

            0 None              开启judge服务
            1 None              停止judge服务
            2 None              重启judge服务
            3 (sid, rejudge)    判题任务请求
    """
    RUN = False
    judge_task = None
    judge_queue = {}
    judge_consumers = {}

    def __init__(self):
        super(JudgeServer, self).__init__()
        self.mysql = MySQL()
        JudgeServer.judge_task = Queue(Task_Limit)

    def judge_start(self):
        if not len(JudgeServer.judge_consumers):
            self.make_judge_queue()
        JudgeServer.RUN = True

    def judge_stop(self):
        for oj in JudgeServer.judge_queue:
            for x in range(JudgeServer.judge_queue[oj].maxsize):
                JudgeServer.judge_queue[oj].put((0, None))
        while not self.all_stop():
            pass
        JudgeServer.judge_queue = {}
        JudgeServer.judge_consumers = {}
        JudgeServer.RUN = False

    def judge_restart(self):
        self.judge_stop()
        self.judge_start()

    def make_judge_queue(self):
        JudgeServer.judge_queue[OJ_NAME] = Queue(Local_Judge_Limit)
        JudgeServer.judge_consumers[OJ_NAME] = []
        for i in range(Local_Judge_Limit):
            JudgeServer.judge_consumers[OJ_NAME].append(JudgeConsumer(OJ_NAME, path_index=i))
            JudgeServer.judge_consumers[OJ_NAME][-1].setDaemon(True)
            JudgeServer.judge_consumers[OJ_NAME][-1].start()
        oj_list = self.mysql.query("SELECT DISTINCT oj FROM core_judge_account WHERE defunct=0")
        for x in oj_list:
            oj = x[0]
            JudgeServer.judge_consumers[oj] = []
            judge_account = self.mysql.query(
                "SELECT username, password FROM core_judge_account WHERE oj='%s' AND defunct=0" % oj)
            JudgeServer.judge_queue[oj] = Queue(len(judge_account))
            for username, password in judge_account:
                JudgeServer.judge_consumers[oj].append(JudgeConsumer(oj, username=username, password=password))
                JudgeServer.judge_consumers[oj][-1].setDaemon(True)
                JudgeServer.judge_consumers[oj][-1].start()

    def all_stop(self):
        return "JudgeConsumer" not in "".join([str(x.__class__) for x in threading.enumerate()])

    def run(self):
        if not len(JudgeServer.judge_consumers):
            self.judge_start()
        while True:
            task = JudgeServer.judge_task.get()
            operator = task[0]
            info = task[1:]
            if operator == '0':
                self.judge_start()
            elif operator == '1':
                self.judge_stop()
            elif operator == '2':
                self.judge_restart()
            elif operator == '3':
                if JudgeServer.RUN:
                    new_judge = JudgeProducer(info)
                    new_judge.start()
            else:
                pass


class JudgeProducer(threading.Thread):
    def __init__(self, info):
        super(JudgeProducer, self).__init__()
        self.sid = info[0]
        self.rejudge = int(info[1])
        self.mysql = MySQL()
        self.oj = None
        self.pid = None
        self.uid = None
        self.judge_type = None
        self.get_info()
        self.update_status()

    def get_info(self):
        try:
            result = self.mysql.query("SELECT problem_id, user_id FROM status_solve WHERE id = '%s'" % self.sid)
        except MySQLQueryError:
            raise Exception
        try:
            self.pid = result[0][0]
            self.uid = result[0][1]
        except (IndexError, TypeError):
            raise Exception
        result = self.mysql.query("SELECT judge_type, oj FROM problem_problem WHERE id = '%s'" % self.pid)
        try:
            self.judge_type = result[0][0]
            self.oj = result[0][1]
        except IndexError:
            raise MySQLQueryError

    def update_status(self):
        self.mysql.update("UPDATE status_solve SET status = 'Queuing' WHERE id = '%s'" % self.sid)

    def run(self):
        try:
            JudgeServer.judge_queue[self.oj].put((1, (self.sid, self.pid, self.uid, self.judge_type)))
        except KeyError:
            pass


class JudgeConsumer(threading.Thread):
    """
        判题请求队列
        请求格式：
            [operator (task)]
            [操作数 (任务消息)]

            0 None                            停止判题线程
            1 (sid, pid, uid, judge_type)     判题任务请求
    """

    def __init__(self, oj, path_index=None, username=None, password=None):
        super(JudgeConsumer, self).__init__()
        self.mysql = MySQL()
        self.oj = oj
        self.run_path = None
        self.sid = None
        self.pid = None
        self.uid = None
        self.problem_id = None
        self.last_result = None
        self.language = None
        self.code = None
        if path_index is not None:
            self.run_path = Local_PATH + '/work/run' + str(path_index)
            if not os.path.exists(self.run_path):
                make_dir(self.run_path)
        if username is not None and password is not None:
            self.username = username
            self.password = password
            self.last_sid = self.get_last_sid()

    def get_ready(self, info):
        self.sid, self.pid, self.uid, self.last_result = info
        self.mysql.update("UPDATE status_solve SET status = 'Judging' WHERE id = '%s'" % self.sid)
        result = self.mysql.query("SELECT language, code  FROM status_solve WHERE id = '%s'" % self.sid)
        self.language = result[0][0]
        self.code = result[0][1]
        result = self.mysql.query("SELECT problem_id  FROM problem_problem WHERE id = '%s'" % self.pid)
        self.problem_id = result[0][0]
        if self.run_path is not None:
            result = self.mysql.query(
                "SELECT time_limit_c, time_limit_java, memory_limit_c, memory_limit_java, data_number FROM problem_problem WHERE id = '%s'" % self.pid)
            time_limit_c = result[0][0]
            time_limit_java = result[0][1]
            memory_limit_c = result[0][2]
            memory_limit_java = result[0][3]
            data_number = result[0][4]
            data_path = Data_PATH + str(self.pid)
            if not os.path.exists(data_path):
                make_dir(data_path)
            code_path = self.run_path + '/Main.' + Language_Map[result[0][0]][1]
            file(code_path, 'w+').write("%s" % code)
            # f = os.popen('./night %s %s %s %s %s %s %s %s' % (
            #     self.language, self.run_path, self.data_path, self.judge_type, self.time_limit_c, self.time_limit_java,
            #     self.memory_limit_c, self.data_number))
            # self.data = f.readline()
            # f.close()

    def get_last_sid(self):
        ac = JudgeAccess(self.oj, self.username, self.password)
        return ac.get_last_sid()

    def judge(self):
        if self.run_path is None:
            vj = VirtualJudge(
                self.username,
                self.password,
                self.last_sid,
                self.language,
                self.code,
                self.oj,
                self.problem_id,
                self.sid
            )
            vj.judge()
        else:
            pass

    def judge_over(self):
        if self.run_path is not None:
            if self.run_path is not "":
                os.system("rm -rf %s/*" % self.run_path)
        else:
            self.last_sid = self.get_last_sid()

    def run(self):
        while True:
            message = JudgeServer.judge_queue[self.oj].get()
            operator, info = message
            if operator == 0:
                return
            elif operator == 1:
                self.get_ready(info)
                self.judge()
                self.judge_over()


def make_dir(path):
    if not os.path.exists(path):
        make_dir('/'.join(os.path.join(path.split('/')[:-1])))
        os.mkdir(path)
