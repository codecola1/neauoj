#coding=utf-8
__author__ = 'Code_Cola'

'''
0   ACM判题模式
1   vjudge
2   单组数据判题
3   程序填空
4   看程序写输出
'''

from status.models import Solve
from core.support.log_main import Log
from core.robot.vjudge import Vjudge


logging = Log()


class Judge:
    def __init__(self, sid):
        try:
            self.solve = Solve.objects.get(id=sid)
            self.problem = self.solve.problem
            self.user = self.solve.user
            self.code = self.solve.code
        except:
            logging.warning("No Such sid!!!<" + str(sid) + ">")
            return
        self.main()

    def main(self):
        if self.problem.judge_type == 0:
            pass
        elif self.problem.judge_type == 1:
            pass
        elif self.problem.judge_type == 2:
            pass
        elif self.problem.judge_type == 3:
            pass
        elif self.problem.judge_type == 4:
            pass