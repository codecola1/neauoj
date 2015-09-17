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


logging = Log()
vqueue = Queue(5)
queue = Queue(5)


class Producer(threading.Thread):
    def __init__(self, sid):
        threading.Thread.__init__(self)
        self.sid = sid
        self.mysql = Connect()
        result = self.mysql.query("SELECT problem_id, user_id FROM status_solve WHERE id = '%s'" % sid)
        self.pid = result[0][0]
        self.uid = result[0][1]
        self.mysql.update("UPDATE status_solve SET status = 'Queuing' WHERE id = '%s'" % self.sid)
        result = self.mysql.query("SELECT judge_type FROM problem_problem WHERE id = '%s'" % self.pid)
        self.judge_type = result[0][0]

    def run(self):
        if self.judge_type == 0:
            pass
        elif self.judge_type == 1:
            vqueue.put((self.sid, self.pid, self.uid))
        elif self.judge_type == 2:
            pass
        elif self.judge_type == 3:
            pass
        elif self.judge_type == 4:
            pass


class Consumer(threading.Thread):
    def __init__(self, index):
        threading.Thread.__init__(self)
        self.index = index

    def run(self):
        pass


class vConsumer(threading.Thread):
    def __init__(self, index):
        threading.Thread.__init__(self)
        self.index = str(index)
        self.mysql = Connect()

    def run(self):
        while True:
            self.sid, self.pid, self.uid = vqueue.get()
            self.judge()

    def judge(self):
        result = self.mysql.query("SELECT oj FROM problem_problem WHERE id = '%s'" % self.pid)
        self.oj = result[0][0]
        result = self.mysql.query(
            "SELECT username, password FROM core_judge_account WHERE oj = '%s' AND user_index = '%s'" % (
                self.oj, self.index))
        username = result[0][0]
        password = result[0][1]
        v = Vjudge(self.sid, username, password)
        v.run()


if __name__ == '__main__':
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
        sid = connection.recv(1024)
        new_judge = Producer(sid)
        new_judge.start()
        connection.send('Receive SID: %s!' % sid)
        connection.close()
    server.close()