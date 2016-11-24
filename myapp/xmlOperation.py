# -* - coding:utf8 -* -
'''
@author: zhangfujun
@time:10/18/16 16:45
'''

import sys
sys.path.append('.')
import  xml.etree.ElementTree as ET
from xml.etree.ElementTree import tostring
from xml.dom import minidom
from myapp.models import Execution, TestCases, TestSteps, Tasks, Element, Page, TaskLog
from myapp.database import db_session, engine


def createXml(taskid, excuteid):
    root = ET.Element('testSuites')
    # allcase = Execution.query.filter(Execution.executeid == excuteid).order_by(Execution.caseid and Execution.stepid).all()
    allcase = Tasks.query.filter(Tasks.id == taskid).first()
    cases = list(eval(allcase.tcs)) if len(allcase.tcs) > 1 else [allcase.tcs, ]
    root.set('count', str(len(cases)))
    root.set('exeid', str(excuteid))
    root.set('suiteName', Tasks.query.filter(Tasks.id == taskid).first().name)
    locator = ''
    for case in cases:
        tc = TestCases.query.filter(TestCases.id == case).first()
        xtc = ET.SubElement(root, 'test', {'name': tc.title, 'caseid': str(tc.id)})  # case level
        tss = TestSteps.query.filter(TestSteps.caseid == tc.id).order_by(TestSteps.sort.asc()).all()
        for ts in tss:
            page = Page.query.filter(Page.pagename == ts.page).first()
            ele = Element.query.filter(
                (Element.name == ts.element).__and__(Element.pageid == page.id)).first()  # step level
            if ele is not None:
                locator = ele.locator if ele.locator else ''
            action = ts.action
            inputValue = ts.value if ts.value else ''
            attr = ts.attr if ts.attr else ''
            xstc = ET.SubElement(xtc, 'step',
                                 {'id': str(ts.id), 'locator': locator, 'action': action, 'inputValue': inputValue,
                                  'attr': attr})
    # tree = ET.ElementTree(root)
    text = '<?xml version="1.0" encoding="utf-8" ?><!DOCTYPE testSuites PUBLIC "-//zhangfujun private//sparrow framework 0.1//EN" "http://10.7.243.110:8080/static/mydtd.dtd">' + tostring(root, 'utf-8')
    executeCommand = TaskLog(taskid, excuteid, text)
    db_session.add(executeCommand)
    db_session.commit()
    tree = ET.ElementTree(root)
    tree.write('output.xml', 'utf-8')
    print 'create case xml finished....'


def postWEBui():
    pass


if __name__ == "__main__":
    createXml(1, 18)

    a = '''<?xml version="1.0"?>
    <data>
        <country name="Liechtenstein">
            <rank>1</rank>
            <year>2008</year>
            <gdppc>141100</gdppc>
            <neighbor name="Austria" direction="E"/>
            <neighbor name="Switzerland" direction="W"/>
        </country>
        <country name="Singapore">
            <rank>4</rank>
            <year>2011</year>
            <gdppc>59900</gdppc>
            <neighbor name="Malaysia" direction="N"/>
        </country>
        <country name="Panama">
            <rank>68</rank>
            <year>2011</year>
            <gdppc>13600</gdppc>
            <neighbor name="Costa Rica" direction="W"/>
            <neighbor name="Colombia" direction="E"/>
        </country>
    </data>'''

    b = ET.fromstring(a)
    '''print b.tag
    print b.attrib
    for child in b:
        print child.tag, child.attrib
    print b[0][2].text
    for neigbour in b.iter('neighbor'):
        print neigbour.attrib
    print '----'
    for country in b.findall('country'):
        rand = country.find('rank').text
        name = country.get('name')
        print name, rand'''

    '''for rank in b.iter('rank'):
        new_r = int(rank.text) +1
        rank.text = str(new_r)
        rank.set('update','yes')
    for country in b.findall('country'):
        rank = int(country.find('rank').text)
        if rank > 50:
            b.remove(country)

    tree = ET.ElementTree(b)
    tree.write('output.xml')'''
