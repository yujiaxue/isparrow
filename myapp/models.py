# -* - coding:utf8 -* -
from myapp.database import Base
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

GMT_FORMAT = '%a, %d %b %Y %H:%M:%S GMT'
MY_FORMAT = '%Y/%m/%d %H:%M:%S'


def date_format(stringdate):
    # return datetime.strftime(datetime.strptime(stringdate,GMT_FORMAT ), MY_FORMAT)
    return datetime.strftime(stringdate, MY_FORMAT)


class Page(Base):
    __tablename__ = 'page'
    id = Column(Integer, primary_key=True)
    pagename = Column(String, )
    chinese = Column(String, )
    desc = Column(String, )
    author = Column(String, )
    createtime = Column(DateTime, )
    updatetime = Column(DateTime, )

    def __init__(self, name=None, chi=None, desc=None, author=None, update=datetime.now()):
        self.pagename = name
        self.chinese = chi
        self.desc = desc
        self.author = author
        self.updatetime = update
        self.createtime = datetime.now()

    def __repr__(self):
        return '<page %r>' % (self.pagename)

    def to_json(self):
        return {
            'id': self.id,
            'pagename': self.pagename,
            'chinese': self.chinese,
            'desc': self.desc,
            'author': self.author,
            'createtime': date_format(self.createtime),
            'updatetime': date_format(self.updatetime)
        }


class Element(Base):
    __tablename__ = 'elementofpage'
    id = Column(Integer, primary_key=True, nullable=False)
    pageid = Column(Integer, nullable=False)
    name = Column(String, )
    locator = Column(String, )
    chinese = Column(String, )
    type = Column(String, )
    createtime = Column(DateTime, )
    updatetime = Column(DateTime, )

    def __init__(self, pid=None, name=None, locator=None, chinese=None, type=None, update=datetime.now()):
        self.pageid = pid
        self.name = name
        self.locator = locator
        self.chinese = chinese
        self.type = type
        self.updatetime = update
        self.createtime = datetime.now()

    def __str__(self):
        return 'element is  ', self.name, self.locator, self.type, self.chinese, self.updatetime

    def tojson(self):
        return {
            'id': self.id,
            'pageid': self.pageid,
            'name': self.name,
            'locator': self.locator,
            'chinese': self.chinese,
            'type': self.type,
            'createtime': date_format(self.createtime),
            'updatetime': date_format(self.updatetime)
        }


class TestCases(Base):
    __tablename__ = 'testcase'
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    author = Column(String, default='QA')
    createtime = Column(DateTime, )
    updatetime = Column(DateTime, )

    def __init__(self, title, author='QA', updatetime=datetime.now()):
        self.title = title
        self.author = author
        self.createtime = datetime.now()
        self.updatetime = updatetime

    def to_json(self):
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'createtime': date_format(self.createtime),
            'updatetime': date_format(self.updatetime),
            'progress': '90'
        }

    def querystatus(self, taskid):
        excute = Excute.query.filter(Excute.taskid == taskid).order_by(Excute.id.desc()).first()
        status = None
        if excute:
            status = Execution.query.filter((Execution.caseid == self.id).__and__(Execution.stepid == 0).__and__(
            Execution.executeid == excute.id)).first()
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'createtime': date_format(self.createtime),
            'updatetime': date_format(self.updatetime),
            'progress': '90',
            'status': status.status if status else 'ready'
        }


class TestSteps(Base):
    __tablename__ = 'teststeps'
    id = Column(Integer, primary_key=True, nullable=False)
    sort = Column(Integer, nullable=False)
    caseid = Column(Integer, nullable=False)
    # stepid = Column(Integer, nullable=False)
    page = Column(String, nullable=False)
    element = Column(String, nullable=False)
    action = Column(String, nullable=False)
    value = Column(String, nullable=True)
    attr = Column(String, )
    label = Column(Integer, )
    createtime = Column(DateTime, default=datetime.now())
    updatetime = Column(DateTime, default=datetime.now())

    def __init__(self, sort, caseid, page, element, action, value=None, attr=None, label=1, updatetime=datetime.now()):
        self.sort = sort
        self.caseid = caseid
        self.page = page
        self.element = element
        self.action = action
        self.value = value
        self.attr = attr
        self.label = label
        self.updatetime = updatetime
        self.createtime = datetime.now()

    def tojson(self):
        return {
            'id': self.id,
            'sort': self.sort,
            'caseid': self.caseid,
            'page': self.page,
            'element': self.element,
            'action': self.action,
            'attr': self.attr,
            'value': self.value
        }


class Tasks(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, nullable=False, primary_key=True)
    name = Column(String, nullable=False)
    author = Column(String, )
    tcs = Column(String, )
    total = Column(Integer, )
    exetime = Column(Integer, )
    status = Column(String, )
    createtime = Column(DateTime, )
    updatetime = Column(DateTime, )

    def __init__(self, name, tcs, total, exetime=0, author=None, status='ready', updatetime=datetime.now()):
        self.name = name
        self.tcs = tcs
        self.total = total
        self.author = author
        self.exetime = exetime
        self.status = 'ready'
        self.createtime = datetime.now()
        self.updatetime = updatetime

    def tojson(self):
        return {
            'id': self.id,
            'name': self.name,
            'author': self.author,
            'tcs': self.tcs,
            'total': self.total,
            'exetime': self.exetime,
            'createtime': date_format(self.createtime),
            'updatetime': date_format(self.updatetime)
        }


class Execution(Base):
    __tablename__ = 'execution'
    id = Column(Integer, nullable=False, primary_key=True)
    executeid = Column(Integer)
    caseid = Column(Integer, )
    stepid = Column(Integer, )
    status = Column(String, )
    log = Column(String, )
    imageurl = Column(String, )
    createtime = Column(DateTime, )
    updatetime = Column(DateTime, )

    def __init__(self, eid, cid, sid, status='unexcute', log='', imageurl='', updatetime=datetime.now()):
        self.executeid = eid
        self.caseid = cid
        self.stepid = sid
        self.status = status
        self.log = log
        self.imageurl = imageurl
        self.createtime = datetime.now()
        self.updatetime = updatetime

    def logtable(self):
        t = TestSteps.query.filter((TestSteps.caseid == self.caseid).__and__(TestSteps.id == self.stepid)).first()
        return {
            'executeid': self.executeid,
            'caseid': self.caseid,
            'stepid': self.stepid,
            'status': self.status,
            'log': self.log if self.log else '',
            'imageurl': self.imageurl if self.imageurl else '',
            'sort': t.id if t else 0,
            'step': '%s.%s.%s.%s.%s' % (
            t.page, t.element, t.action, t.value if t.value else '', t.attr if t.attr else '')
        }


class Excute(Base):
    __tablename__ = 'excute'
    id = Column(Integer, nullable=False, primary_key=True)
    taskid = Column(Integer, )
    casecount = Column(Integer, )
    failcase = Column(Integer, )
    successcase = Column(Integer, )
    skipcase = Column(Integer, )
    excutetime = Column(Integer, )
    createtime = Column(DateTime, default=datetime.now())
    updatetime = Column(DateTime, default=datetime.now())

    def __init__(self, taskid, casecount, failcase=0, successcase=0, skipcase=0, excutetime=0,
                 updatetime=datetime.now()):
        self.taskid = taskid
        self.casecount = casecount
        self.successcase = successcase
        self.failcase = failcase
        self.skipcase = skipcase
        self.excutetime = excutetime
        self.updatetime = updatetime
        self.createtime = datetime.now()

    def to_json(self):
        return {
            "id": self.id,
            "taskid": self.taskid,
            "casecount": self.casecount,
            "failcase": self.failcase,
            "successcase": self.successcase,
            "skipcase": self.skipcase,
            "excutetime": self.excutetime,
            "createtime": date_format(self.createtime),
            "updatetime": date_format(self.updatetime)
        }


class Actions(Base):
    __tablename__ = 'operation'
    id = Column(Integer, nullable=False, primary_key=True)
    operation = Column(String, )
    value = Column(String, )
    createtime = Column(DateTime, )
    updatetime = Column(DateTime, )


class TaskLog(Base):
    __tablename__ = 'tasklogs'
    id = Column(Integer, nullable=False, primary_key=True)
    taskid = Column(Integer, )
    executeid = Column(Integer, )
    xmltext = Column(String, )
    createtime = Column(DateTime, )
    updatetime = Column(DateTime, )

    def __init__(self, tid, eid, xmltext, updatetime=datetime.now()):
        self.taskid = tid
        self.executeid = eid
        self.xmltext = xmltext
        self.createtime = datetime.now()
        self.updatetime = updatetime
