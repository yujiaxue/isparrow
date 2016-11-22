# -* -coding:utf-8 -* -
'''
@author: zhangfujun
@time:11/21/16 16:10
'''

import MySQLdb,re
def generateList():
    sourcefile = 'your file'
    regex = r'public .+ .+\(.*\)'
    reg = re.compile(regex)
    with open(sourcefile) as f:
        data = f.read()
        result = reg.findall(data)
    print 'result length is     ', len(result)
    return result,data


def docGenerate():
    result,data = generateList()
    tempindex = 0
    try:
        dbo = insertOperation()
        for l in result:
            index = data.index(l)
            temp = data[tempindex:index]
            anoindex = temp.rindex('/**')
            annotation = temp[anoindex:index]
            annotation = annotation.replace('*', '').replace('\n', '')
            desc = ''
            try:
                desc = annotation[1:annotation.index('@')]
            except Exception as e:
                if e.message=='substring not found':
                    desc = annotation[1:-2]
            operation = l.split('(')[0].split(' ')[-1]
            value= l.split('(')[1][0:-1]
            descrition = desc.strip()
            print operation,'-',value.strip(),'-',descrition.strip()
            dbo.execsql(operation,value.strip(),descrition.strip())
            result = ''
            tempindex=anoindex
    except Exception as e:
        print 'aaa.'
        print e.__class__
        print l

def diffdb():
    result,data = generateList()
    dbo = insertOperation()
    result = [r.split('(')[-2].split(' ')[-1] for r in result ]
    print result
    dbo.querydiff(result)
class insertOperation():
    def __init__(self):
        self.conn = MySQLdb.Connect(host='10.7.243.110', user='root', passwd='123456', db='UIAUTO', charset='utf8')
        self.conn.autocommit(True)
        self.cursor = self.conn.cursor()
    #result = cursor.execute('insert operation(operation,value,description) value(%s,%s,%s)'%())
    def execsql(self,operation,value,description):
        #if operation in ('assertCssValue','assertCssColor'):
        #sql = 'insert operation(operation,value,description) value("%s","%s","%s")'%(operation,value,description)
        sql = 'update operation set description="%s" where operation="%s"'%(description,operation)
        print sql
        self.cursor.execute(sql)
    def querydiff(self,result):
        sql = 'select operation  from operation where operation in ("'+'","'.join(result)+'")'
        print sql
        self.cursor.execute(sql)
        a = self.cursor.fetchall()
        ops = [operation[0].encode('utf8') for operation in a]
        print ops
        print result
        m = ops+result
        for n in m:
            if m.count(n) <2:
                print n
if __name__ == "__main__":
    docGenerate()
    #diffdb()

