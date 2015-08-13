__author__ = 'Code_Cola'

from problem.robot.get_problem import Down_problem

test = Down_problem('hdu', 2345)
if test.right:
    test.get_info()