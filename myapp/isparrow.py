# -* - coding:utf8 -* -
from flask import render_template, jsonify, request, redirect, url_for
from datetime import datetime
from myapp import myapplication
import threading
from time import sleep
import json, urllib2, urllib, socket

from myapp.database import db_session, engine
from myapp.models import Page, Element, TestCases, TestSteps, Tasks, Execution, Excute, Actions, TaskLog,statistic
import xmlOperation


# from myapp import model1,myapp,db
#
# @myapp.route('/deletepage',methods=['POST','GET'])
# def delete():
#     t = model1.Page('hah33a','hah33a')
#     t.save()
#     #db.session.add(t)
#     #db.session.commit()
#     return 'ok'
# @myapp.route("/query")
# def qu():
#     page = model1.Page.query.all()
#     for p in page:
#         print p
#
#     return 'ok1'


@myapplication.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


# region
'''testcases'''


@myapplication.route('/showcase')
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
    print mylist
    return render_template('testcases.html', a={'pagec': u'测试用例', 'showcase': True, 'mylist': mylist})


@myapplication.route('/addcasePage')
def addCase():
    return render_template('addCase.html', a={'pagec': u'编辑用例', 'addcase': True})


@myapplication.route('/addCase', methods=['POST', ])
def addOneCase():
    data = request.form
    title = data.get('caseName')
    if not title:
        return jsonify(status='fail')
    tc = TestCases(title=title)
    db_session.add(tc)
    db_session.commit()
    return jsonify(status='success')


@myapplication.route('/getCases')
def queryCase():
    tc = TestCases.query.order_by(TestCases.createtime.desc()).all()
    return jsonify(status='success', tc=[t.to_json() for t in tc])


# endregion

'''
page's method
'''


@myapplication.route('/getpages')
def getAllPages():
    pages = Page.query.order_by(Page.pagename.asc()).all()
    return jsonify(status='success', pages=[p.pagename for p in pages])


@myapplication.route('/queryPage')
def queryPage():
    pages = Page.query.order_by(Page.id.desc()).all()
    return jsonify(status='success', pages=[p.to_json() for p in pages])


@myapplication.route('/addPage', methods=['post'])
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


@myapplication.route('/addElement', methods=['post', ])
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


@myapplication.route('/deleteElement', methods=['post', ])
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


@myapplication.route('/getcasesteps/<cid>')
def getSteps(cid):
    steps = []
    if cid:
        steps = TestSteps.query.filter((TestSteps.caseid == cid).__and__(TestSteps.label== 1)).order_by(TestSteps.sort.asc()).all()
    if steps:
        return jsonify(steps=[step.tojson() for step in steps], status='success')
    else:
        return jsonify(status='success', steps=[])


@myapplication.route('/addonestep', methods=['post'])
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


@myapplication.route('/getstepnum', methods=['post'])
def getStepNum():
    form = request.form
    cid = form.get('cid')
    num = TestSteps.query.filter(TestSteps.caseid == cid).count()
    return jsonify(status='success', num=num)


@myapplication.route('/deleteItem', methods=['post'])
def deleteItem():
    form = request.form
    sid = form.get('id')

    ts = TestSteps.query.filter(TestSteps.id==sid).first()
    ts.label=0
    # db_session.delete(ts)
    db_session.add(ts)
    db_session.commit()
    return jsonify({'status':'success'})


@myapplication.route('/updateonestep',methods=['post'])
def editItem():
    form = request.form
    id = form.get('id')
    sort = form.get('sid')
    cid = form.get('cid')
    page = form.get('page')
    element = form.get('element')
    action = form.get('action')
    value = form.get('input')
    attr = form.get('attr')

    if not cid or not page or not action:
        return jsonify({'status': 'fail'})

    step = TestSteps.query.filter(TestSteps.id==id).first()
    step.sort=sort
    step.cid=cid
    step.page = page
    step.element = element
    step.action = action
    step.value = value
    step.attr = attr
    db_session.add(step)
    db_session.commit()
    return jsonify({'status':'success'})

# endregion




# region
'''task'''


@myapplication.route('/addtask', methods=['post'])
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


@myapplication.route('/tasks')
def showTasks():
    t = Tasks.query.order_by(Tasks.id.desc()).all()
    return render_template('tasks.html', a={'pagec': u'任务执行', 'showtask': True, 'tasks': [m.tojson() for m in t]})


@myapplication.route('/tasks/<tid>')
def oneTask(tid):
    t = Tasks.query.filter(Tasks.id == tid).first()
    tcs = []
    if len(t.tcs) < 2:
        tcs = [t.tcs, ]
    else:
        tcs = list(eval(t.tcs))
    exet = TestCases.query.filter(TestCases.id.in_(tcs)).all()
    # 执行ID 传入 查询状态


    ''''''
    return render_template('onetask.html',
                           a={'pagec': t.name, 'tid': tid, 'status': t.status,
                              'case': [c.querystatus(tid) for c in exet]})


@myapplication.route('/modifyTask/<tid>')
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


@myapplication.route('/editTask/<tid>', methods=['post', ])
def editTask(tid):
    form = request.form
    tcs = form.get('tcs')
    task = Tasks.query.filter(Tasks.id == tid).first()
    task.tcs = tcs
    task.total = len(tcs.split(','))
    db_session.add(task)
    db_session.commit()
    return redirect(url_for('oneTask', tid=tid))


@myapplication.route('/tasks/<tid>/<cid>')
def tasklog(tid, cid):
    t = Excute.query.filter(Excute.taskid == tid).order_by(Excute.id.desc()).first()
    if t:
        execution = Execution.query.filter((Execution.executeid == t.id).__and__(Execution.caseid == cid)).all()
        log = [l.logtable() for l in execution if l.stepid]
    else:
        log = []
    caseName = TestCases.query.filter(TestCases.id == cid).first()
    return render_template('tasklog.html',
                           a={'pagec': caseName.title, 'log': log})


# endregion



# region
@myapplication.route('/execute', methods=['post'])
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
        tce = Execution(excute.id, tc.id, 0, 'undone')
        db_session.add(tce)
        db_session.commit()
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
    xmlOperation.createXml(taskid, excuteid)
    handlerRequest(taskid, excuteid)
    print 'ok.....'


@myapplication.route('/progress/<tid>')
def progress(tid):
    exc = Excute.query.filter(max(Excute.taskid)).first();
    execution = Execution.query.filter(Execution.id == exc.id).first();


# endregion


@myapplication.route('/')
def hello_world():
    caseStatistic = statistic()
    return render_template("index.html",a =caseStatistic)


@myapplication.route('/element/<pid>')
def element(pid):
    page = Page.query.filter(Page.id == pid).first()
    if (not page):
        return render_template('element.html', a={'pagec': u'元素定位器', 'ele': None})
    ele = Element.query.filter(Element.pageid == pid).all()
    if len(ele) == 0 or not ele:
        return render_template('element.html', a={'pagec': page.chinese, 'ele': None})
    return render_template('element.html', a={'pagec': page.chinese, 'pid': page.id, 'ele': ele})


@myapplication.route('/element/item/<pid>')
def elementItem(pid):
    ele = Element.query.filter(Element.pageid == pid).all()
    return jsonify(status='success', elements=[e.tojson() for e in ele])


@myapplication.route('/pageditor')
def edit_page():
    '''p= Page.query.all()
    print p'''
    content = {'title': u'页面对象', 'pageeditor': True}
    return render_template("pageEditor.html", a=content)


@myapplication.route('/api/todo')
def todo():
    content = {'author': 'fujun.zhang@superjia.com'}
    return json.dumps(content)


@myapplication.errorhandler(404)
def not_found(error):
    return render_template('404.html')


@myapplication.route('/getactions')
def getActions():
    actions = Actions.query.order_by(Actions.operation.asc()).all()
    return jsonify(status='success', actions=[action.operation for action in actions])


@myapplication.route('/pagemapelement')
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


# region
'''task log'''


@myapplication.route('/getcasexml/<tid>/<eid>')
def getCaseXml(tid, eid):
    log = TaskLog.query.filter((TaskLog.taskid == tid).__and__(TaskLog.executeid == eid)).first()
    if log:
        return log.xmltext
    else:
        return 'no result'


def handlerRequest(tid, eid):
    params = urllib.urlencode({'tid': tid, 'eid': eid})
    f = urllib.urlopen("http://10.7.242.68:8080/hellof?%s" % params)
    print f.read()


# endregion


# region
''' 日志功能'''


@myapplication.route('/task/log/<tid>')
def logChat(tid):
    task = Tasks.query.filter(Tasks.id == tid).first()
    log = Excute.query.filter(Excute.taskid == tid).order_by(Excute.id.desc()).all()
    return render_template('log.html', a={'pagec': task.name, 'logs': [l.to_json() for l in log]})


@myapplication.route('/execute/log/<eid>')
def oneLog(eid):
    log = Execution.query.filter(Execution.executeid == eid).order_by(Execution.id.desc()).all()
    return render_template('tasklog.html', a={'pagec': u'', 'log': [l.logtable() for l in log if l.stepid]})


@myapplication.route('/alllogs')
def allLogs():
    logs = Excute.query.order_by(Excute.id.desc()).all()
    return render_template('alllog.html', a={'pagec': u'日志', 'logs': [l.to_json() for l in logs]})


# endregion


# region
'''function'''


@myapplication.route('/customFuction')
def customFuction():
    return render_template('customFucntion.html', a={'pagec': u'自定义功能'})


# endregion

#region
'''grid '''
def queryGrid():
    baseUrl = "http://10.7.242.68:3333/grid/register"
    dd = urllib.urlopen(baseUrl)
    print dd

#endregion


#region
'''doc '''
@myapplication.route('/alldoc')
def mydoc():
    return render_template('mydoc.html',a={'pagec':u'使用说明'})

@myapplication.route('/webuifunctiondescription')
def functiondescription():
    allfunction = Actions.query.all()
    return render_template("funcdesc.html",a={'pagec':u'函数列表','action':[func.to_json() for func in allfunction]})

@myapplication.route('/useNavigation')
def useNavigation():
    import  markdown2
    useNaviation = markdown2.markdown('*this is  a useNavigation*')
    return render_template('useNavigation.html',a={'pagec':u'使用向导','useNaviation':useNaviation})
#endregion


@myapplication.route('/aaaaa')
def aaaaa():
    return render_template('test1.html',a={'pagec':u'asdfsdf',})


if __name__ == '__main__':
    myapplication.debug = True
    ip = socket.gethostbyname(socket.gethostname())
    if ip == '10.7.243.110':
        myapplication.run()
    else:
        myapplication.run(host='127.0.0.1', port=5000)
