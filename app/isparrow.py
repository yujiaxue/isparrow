# -* - coding:utf8 -* -
from _mysql_exceptions import IntegrityError
from flask import render_template, jsonify, request, redirect, url_for
from datetime import datetime
from app import app
import threading
from time import sleep
import json,requests

from app.database import db_session, engine
from app.models import Page, Element, TestCases, TestSteps, Tasks, Execution, Excute, Actions,TaskLog
from utils import createXml


# from app import model1,app,db
#
# @app.route('/deletepage',methods=['POST','GET'])
# def delete():
#     t = model1.Page('hah33a','hah33a')
#     t.save()
#     #db.session.add(t)
#     #db.session.commit()
#     return 'ok'
# @app.route("/query")
# def qu():
#     page = model1.Page.query.all()
#     for p in page:
#         print p
#
#     return 'ok1'


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


# region
'''testcases'''


@app.route('/showcase')
def showCase():
    mylist = {}
    allcase = TestCases.query.order_by(TestCases.id.desc()).all()
    for case in allcase:
        steps = TestSteps.query.filter(TestSteps.caseid == case.id).order_by(TestSteps.sort.asc()).all()
        c = case.to_json()
        s = None
        if steps:
            mysteps = []
            for step in steps:
                mysteps.append(step.tojson())
            s = mysteps
        mylist[case.id] = {'case': c, 'step': s}
    return render_template('testcases.html', a={'pagec': u'测试用例', 'showcase': True, 'mylist': mylist})


@app.route('/addcasePage')
def addCase():
    return render_template('addCase.html', a={'pagec': u'编辑用例', 'addcase': True})


@app.route('/addCase', methods=['POST', ])
def addOneCase():
    data = request.form
    title = data.get('caseName')
    if not title:
        return jsonify(status='fail')
    tc = TestCases(title=title)
    db_session.add(tc)
    db_session.commit()
    return jsonify(status='success')


@app.route('/getCases')
def queryCase():
    tc = TestCases.query.order_by(TestCases.createtime.desc()).all()
    return jsonify(status='success', tc=[t.to_json() for t in tc])


# endregion

'''
page's method
'''


@app.route('/getpages')
def getAllPages():
    pages = Page.query.order_by(Page.pagename.asc()).all()
    return jsonify(status='success', pages=[p.pagename for p in pages])


@app.route('/queryPage')
def queryPage():
    pages = Page.query.order_by(Page.id.desc()).all()
    return jsonify(status='success', pages=[p.to_json() for p in pages])


@app.route('/addPage', methods=['post'])
def addPage():
    form = request.form
    name = form.get('page')
    china = form.get('china')
    desc = form.get('desc')
    if not name:
        return jsonify(status='fail')
    p = Page(name, china, desc)
    db_session.add(p)
    db_session.commit()
    return jsonify(status='success')


# region
'''elements'''


@app.route('/addElement', methods=['post', ])
def addElement():
    form = request.form
    pid = form.get("pid")
    name = form.get('name')
    locator = form.get('locator')
    china = form.get('chinese')
    type = form.get('type')
    if not pid or not name or not locator or not china or not type:
        return jsonify(status='fail')
    try:
        ele = Element(pid, name, locator, china, type)
        db_session.add(ele)
        db_session.commit()
    except Exception as e:
        print e.message
        return jsonify(status='fail', message=e.message)
    return jsonify(status='success')


@app.route('/deleteElement', methods=['post', ])
def deleteElement():
    form = request.form
    eid = form.get('id')
    e = Element.query.filter(Element.id == eid).first()
    db_session.delete(e)
    db_session.commit()
    return jsonify(status='success')


# endregion

# region
'''steps
'''


@app.route('/getcasesteps/<cid>')
def getSteps(cid):
    steps = []
    if cid:
        steps = TestSteps.query.filter(TestSteps.caseid == cid).order_by(TestSteps.sort.asc()).all()
    if steps:
        return jsonify(steps=[step.tojson() for step in steps], status='success')
    else:
        return jsonify(status='success', steps=[])


@app.route('/addonestep', methods=['post'])
def addStep():
    form = request.form
    sort = form.get('sid')
    cid = form.get('cid')
    page = form.get('page')
    element = form.get('element')
    action = form.get('action')
    value = form.get('input')
    attr = form.get('attr')

    if not cid or not page or not action:
        return jsonify({'status': 'fail'})

    # if not element:
    step = TestSteps(sort, cid, page, element, action, value, attr)
    db_session.add(step)
    db_session.commit()
    # return jsonify({'status': 'success'})
    # else:
    #    elementid = Element.query.filter(Element.name==element).first()
    #    elementid=elementid.id
    #    pageid = Page.query.filter(Page.pagename == page).first()
    #    pageid = pageid.id
    # step = TestSteps(sort,cid, page, element, action,value,attr)
    # db_session.add(step)
    # db_session.commit()
    return jsonify({'status': 'success'})


@app.route('/getstepnum', methods=['post'])
def getStepNum():
    form = request.form
    cid = form.get('cid')
    num = TestSteps.query.filter(TestSteps.caseid == cid).count()
    return jsonify(status='success', num=num)


@app.route('/deleteItem', methods=['post'])
def deleteItem():
    form = request.form
    sid = form.get('id')


# endregion




# region
'''task'''


@app.route('/addtask', methods=['post'])
def addTask():
    form = request.form
    name = form.get('name')
    case = form.getlist('tcs[]')
    cn = len(case)
    t = Tasks.query.filter(Tasks.name == name).first()
    if t:
        return jsonify(status='fail', message='该计划名已存在')
    if not name or not case:
        return jsonify(status='fail', message='缺少参数')
    case = ','.join(case)
    task = Tasks(name, case, cn)
    db_session.add(task)
    db_session.commit()

    '''for c in case:
        tsp = TestSteps.query.filter(TestSteps.caseid==c).order_by(TestSteps.id.asc()).all()
        for ts in tsp:
            Execution(t.id,)'''
    # return redirect('/tasks/')
    # return redirect('/tasks/%d'%t.id)
    return jsonify(status='success', id=task.id if task else t.id)


@app.route('/tasks')
def showTasks():
    t = Tasks.query.order_by(Tasks.id.desc()).all()
    return render_template('tasks.html', a={'pagec': u'任务执行', 'showtask': True, 'tasks': [m.tojson() for m in t]})


@app.route('/tasks/<tid>')
def oneTask(tid):
    t = Tasks.query.filter(Tasks.id == tid).first()
    tcs = []
    if len(t.tcs) < 2:
        tcs = [t.tcs, ]
    else:
        tcs = list(eval(t.tcs))
    exet = TestCases.query.filter(TestCases.id.in_(tcs)).all()

    ''''''
    return render_template('onetask.html',
                           a={'pagec': t.name, 'tid': tid, 'status': t.status, 'case': [c.to_json() for c in exet]})


@app.route('/modifyTask/<tid>')
def modifyTask(tid):
    t = Tasks.query.filter(Tasks.id == tid).first()
    tcs = []
    if not t.tcs:
        pass
    elif len(t.tcs) < 2:
        tcs = [int(t.tcs), ]
    else:
        tcs = list(eval(t.tcs, ))
    if tcs:
        tcs = [int(tc) for tc in tcs]
    alltc = TestCases.query.all()

    return render_template('modifytask.html', a={'tid': tid, 'pagec': u'编辑任务', 'checktc': tcs, 'alltc': alltc})


@app.route('/editTask/<tid>', methods=['post', ])
def editTask(tid):
    form = request.form
    tcs = form.get('tcs')
    task = Tasks.query.filter(Tasks.id == tid).first()
    task.tcs = tcs
    task.total=len(tcs.split(','))
    db_session.add(task)
    db_session.commit()
    return redirect(url_for('oneTask', tid=tid))


# endregion



# region
@app.route('/execute', methods=['post'])
def execute():
    tid = request.form.get('tid')
    task = Tasks.query.filter(Tasks.id == tid).first()
    if task.status == 'running':
        return jsonify(status='fail', message='当前任务正在执行,请等待执行完成后')
    task.status = 'running'
    db_session.commit()
    # if hasattr(task.tcs, '__iter__'):
    #    print list(task.tcs)
    # tcs = list(task.tcs) if hasattr(task.tcs,'__iter__') else [task.tcs,]
    excute = Excute(tid, task.total)
    db_session.add(excute)
    db_session.commit()
    tcs = list(eval(task.tcs)) if len(task.tcs) > 1 else [task.tcs, ]
    for cid in tcs:
        tc = TestCases.query.filter(TestCases.id == cid).first()
        tss = TestSteps.query.filter(TestSteps.caseid == tc.id).order_by(TestSteps.sort.asc()).all()
        for ts in tss:
            exe = Execution(excute.id, tc.id, ts.id, 'undone')
            db_session.add(exe)
    db_session.commit()
    t = threading.Thread(target=xmlexport, args=(tid, excute.id))
    t.setDaemon(True)
    t.start()
    print '线程已启动'
    return jsonify(status='success', eid=excute.id)


def xmlexport(taskid, excuteid):
    print taskid, excuteid
    createXml(taskid, excuteid)
    print 'ok.....'


@app.route('/progress/<eid>')
def progress(eid):
    pass


# endregion


@app.route('/')
def hello_world():
    return render_template("index.html")


@app.route('/element/<pid>')
def element(pid):
    page = Page.query.filter(Page.id == pid).first()
    if (not page):
        return render_template('element.html', a={'pagec': u'元素定位器', 'ele': None})
    print page.chinese
    ele = Element.query.filter(Element.pageid == pid).all()
    if len(ele) == 0 or not ele:
        return render_template('element.html', a={'pagec': page.chinese, 'ele': None})
    return render_template('element.html', a={'pagec': page.chinese, 'pid': page.id, 'ele': ele})


@app.route('/element/item/<pid>')
def elementItem(pid):
    print 'pid is ', pid
    ele = Element.query.filter(Element.pageid == pid).all()
    return jsonify(status='success', elements=[e.tojson() for e in ele])


@app.route('/pageditor')
def edit_page():
    '''p= Page.query.all()
    print p'''
    content = {'title': u'页面对象', 'pageeditor': True}
    return render_template("pageEditor.html", a=content)


@app.route('/api/todo')
def todo():
    content = {'author': 'fujun.zhang@superjia.com'}
    return json.dumps(content)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html')


@app.route('/getactions')
def getActions():
    actions = Actions.query.order_by(Actions.operation.asc()).all()
    return jsonify(status='success', actions=[action.operation for action in actions])


@app.route('/pagemapelement')
def pageMapElement():
    mappage = {}
    page = Page.query.all()
    for p in page:
        mappage[p.pagename] = []
    for p in page:
        ele = Element.query.filter(Element.pageid == p.id).order_by(Element.name.asc()).all()
        for el in ele:
            mappage[p.pagename].append(el.name)
    return jsonify(status='success', pageelement=mappage)


#region
'''task log'''
@app.route('/getcasexml/<tid>/<eid>')
def getCaseXml(tid,eid):
    log = TaskLog.query.filter((TaskLog.taskid==tid).__and__(TaskLog.executeid==eid)).first()
    if log:
        return log.xmltext
    else:
        return 'no result'

def handlerRequest():
    r = requests.get('https://github.com/timeline.json')

#endregion


if __name__ == '__main__':
    app.debug = True
    app.run(host='10.7.246.158', port=5000)
