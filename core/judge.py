# coding=utf-8
__author__ = 'Code_Cola'

'''
0   ACM判题模式
1   vjudge
2   单组数据判题
3   程序填空
4   看程序写输出
'''

from support.mysql_join import Connect
from support.log_judge import Log
from vjudge import Vjudge
from Queue import Queue
import threading
import socket
import os
import sys
import random

logging = Log()
vqueue = Queue(5)
queue = Queue(5)
local_path = '/'.join(os.getcwd().split('/')[0:-1])
language_map = {
    'c': ['0', 'c'],
    'c++': ['1', 'cpp'],
    'g++': ['2', 'cc'],
    'java': ['3', 'java'],
}
judge_map = ['Accepted', 'Wrong Answer', 'Presentation Error', 'Compilation Error', 'Time Limit Exceeded',
             'Memory Limit Exceeded', 'Runtime Error']


class Producer(threading.Thread):
    def __init__(self, sid):
        threading.Thread.__init__(self)
        self.sid = sid[0]
        self.rejudge = int(sid[1])
        self.mysql = Connect()
        result = self.mysql.query("SELECT problem_id, user_id FROM status_solve WHERE id = '%s'" % sid[0])
        self.pid = result[0][0]
        self.uid = result[0][1]
        self.last_result = 0
        if not self.rejudge:
            self.mysql.update("UPDATE status_solve SET status = 'Queuing' WHERE id = '%s'" % self.sid)
            self.mysql.update("UPDATE problem_problem SET submit = submit + 1 WHERE id = '%s'" % self.pid)
            self.mysql.update("UPDATE users_info SET submit = submit + 1 WHERE id = '%s'" % self.uid)
        else:
            result = self.mysql.query("SELECT status FROM status_solve WHERE id = '%s'" % self.sid)
            self.last_result = 1 if result == 'Accepted' else 0
        result = self.mysql.query("SELECT judge_type FROM problem_problem WHERE id = '%s'" % self.pid)
        self.judge_type = result[0][0]

    def run(self):
        if self.judge_type == 0:
            queue.put((self.sid, self.pid, self.uid, self.judge_type, self.last_result))
        elif self.judge_type == 1:
            vqueue.put((self.sid, self.pid, self.uid, self.last_result))
        elif self.judge_type == 2:
            queue.put((self.sid, self.pid, self.uid, self.judge_type, self.last_result))
        elif self.judge_type == 3:
            queue.put((self.sid, self.pid, self.uid, self.judge_type, self.last_result))
        elif self.judge_type == 4:
            pass


class Consumer(threading.Thread):
    def __init__(self, index):
        threading.Thread.__init__(self)
        self.index = index
        self.run_path = local_path + '/work/run' + str(index)

    def run(self):
        while True:
            self.sid, self.pid, self.uid, self.judge_type, self.last_result = queue.get()
            self.mysql = Connect()
            self.mysql.update("UPDATE status_solve SET status = 'Judging' WHERE id = '%s'" % self.sid)
            self.judge()
            self.save()
            os.system("rm -rf %s/*" % self.run_path)

    def judge(self):
        result = self.mysql.query(
            "SELECT time_limit_c, time_limit_java, memory_limit_c, memory_limit_java, data_number FROM problem_problem WHERE id = '%s'" % self.pid)
        self.time_limit_c = result[0][0]
        self.time_limit_java = result[0][1]
        self.memory_limit_c = result[0][2]
        self.memory_limit_java = result[0][3]
        self.data_number = result[0][4]
        self.data_path = local_path + '/data/' + str(self.pid)
        result = self.mysql.query("SELECT language, code  FROM status_solve WHERE id = '%s'" % self.sid)
        self.language = language_map[result[0][0]][0]
        code = result[0][1]
        code_path = self.run_path + '/Main.' + language_map[result[0][0]][1]
        fp = open(code_path, "w+")
        fp.write(code)
        fp.close()
        f = os.popen('./night %s %s %s %s %s %s %s %s' % (
            self.language, self.run_path, self.data_path, self.judge_type, self.time_limit_c, self.time_limit_java,
            self.memory_limit_c, self.data_number))
        self.data = f.readline()
        f.close()

    def save(self):
        self.data = self.data.split(' ')
        judge_status = judge_map[int(self.data[0])]
        use_time = self.data[1] if len(self.data) > 1 else 0
        use_memory = random.randint(1700, 3500)
        self.mysql.update(
            "UPDATE status_solve SET status = '%s', use_time = '%s', use_memory = '%s' WHERE id = '%s'" % (
                judge_status, use_time, use_memory, self.sid))
        if judge_status == 'Accepted' and not self.last_result:
            self.mysql.update("UPDATE problem_problem SET solved = solved + 1 WHERE id = '%s'" % self.pid)
            self.mysql.update("UPDATE users_info SET solve = solve + 1 WHERE id = '%s'" % self.uid)


class vConsumer(threading.Thread):
    def __init__(self, index):
        threading.Thread.__init__(self)
        self.index = str(index)

    def run(self):
        while True:
            self.sid, self.pid, self.uid, self.last_result = vqueue.get()
            self.mysql = Connect()
            self.mysql.update("UPDATE status_solve SET status = 'Judging' WHERE id = '%s'" % self.sid)
            self.judge()

    def judge(self):
        result = self.mysql.query("SELECT oj FROM problem_problem WHERE id = '%s'" % self.pid)
        self.oj = result[0][0]
        result = self.mysql.query(
            "SELECT username, password FROM core_judge_account WHERE oj = '%s' AND user_index = '%s'" % (
                self.oj, self.index))
        username = result[0][0]
        password = result[0][1]
        v = Vjudge(self.sid, username, password, self.last_result)
        v.run()


if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf8')
    server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    if os.path.exists('/tmp/judge.sock'):
        os.unlink('/tmp/judge.sock')
    server.bind('/tmp/judge.sock')
    server.listen(0)
    threads = []
    vthreads = []
    for i in range(5):
        t = Consumer(i)
        threads.append(t)
        t = vConsumer(i)
        vthreads.append(t)
    for i in range(5):
        threads[i].setDaemon(True)
        threads[i].start()
        vthreads[i].setDaemon(True)
        vthreads[i].start()
    while True:
        connection, address = server.accept()
        sid = connection.recv(1024).split(' ')
        new_judge = Producer(sid)
        new_judge.start()
        connection.send('Receive SID: %s!' % sid[0])
        connection.close()
    server.close()
