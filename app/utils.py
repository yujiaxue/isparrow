'''
@author: zhangfujun
@time:10/18/16 16:45
'''

import  xml.etree.ElementTree as ET
from app.models import Execution,TestCases,TestSteps,Tasks

def createXml(taskid,excuteid):
    root = ET.Element('testcases')
    #allcase = Execution.query.filter(Execution.executeid == excuteid).order_by(Execution.caseid and Execution.stepid).all()
    allcase = Tasks.query.filter(id==taskid).first()
    cases = list(eval(allcase.tcs)) if len(allcase.tcs) >1 else [allcase.tcs,]
    root.set('count',len(cases))

    for case in cases:
        tc= TestCases.query.filter(id==case).first()
        tc.page,tc.elementmc
        xtc = ET.SubElement(root,'tc',{'name':tc.title,'id':tc.id})
        tss = TestSteps.query.filter(TestSteps.caseid==tc.id).order_by(TestSteps.sort.asc()).all()
        for ts in tss:
            xstc = ET.SubElement(xtc,'ts',{'page'})

if __name__ == "__main__":
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

    for rank in b.iter('rank'):
        new_r = int(rank.text) +1
        rank.text = str(new_r)
        rank.set('update','yes')
    for country in b.findall('country'):
        rank = int(country.find('rank').text)
        if rank > 50:
            b.remove(country)

    tree = ET.ElementTree(b)
    tree.write('output.xml')