'''
@author: zhangfujun
@time:10/10/16 11:01
'''

from flask.blueprints import Blueprint
steps = Blueprint('steps',__name__)

from models import TestSteps

@steps.route('/getcasesteps/<cid>',method=['get',])
def getSteps(cid):
    steps = []
    if cid:
        steps = TestSteps.query.filter(TestSteps.caseid==cid).order_by(TestSteps.sort.asc()).all()
    print steps
    return