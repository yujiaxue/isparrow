# -*- coding:utf-8 -*-
'''
@author: zhangfujun
@time:11/25/16 14:52
'''

from flask_script import  Manager
from myapp import  myapplication
manager = Manager(myapplication)

@manager.command
def case_Statistic():
    print "ok"


if __name__ == "__main__":
    manager.run()
