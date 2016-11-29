'''
@author: zhangfujun
@time:10/10/16 11:01
'''

from flask.blueprints import Blueprint

steps = Blueprint('steps', __name__)

from models import TestSteps


@steps.route('/getcasesteps/<cid>', method=['get', ])
def getSteps(cid):
    steps = []
    if cid:
        steps = TestSteps.query.filter(TestSteps.caseid == cid).order_by(TestSteps.sort.asc()).all()
    print steps
    with open("a.txt") as f:
        pass
    return
def myfunc(mylist):
    print mylist
def myfunc(x):
    print 'x =',

if __name__ == "__main__":
    a = {1L: {'fail': 1L, 'pass': 8L, 'title': u'\u6309\u884c\u653f\u533a\u57df\u540d\u641c\u7d22\u79df\u623f\u623f\u6e90'}, 2L: {'fail': 4L, 'pass': 4L, 'title': u'\u6309\u884c\u653f\u533a\u57df\u540d\u641c\u7d22\u4e8c\u624b\u623f\u623f\u6e90'}, 3L: {'fail': 0, 'pass': 0, 'title': u'\u5df2\u767b\u9646\u72b6\u6001\u7ea6\u770b\u79df\u623f\u623f\u6e90'}, 4L: {'fail': 0, 'pass': 0, 'title': u'\u672a\u767b\u5f55\u72b6\u6001\u7ea6\u770b\u623f\u6e90'}}
    dict = sorted(a.iteritems(),key=lambda x:x[1].get('fail'),reverse=True)
    print dict


