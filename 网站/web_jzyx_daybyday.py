import pymysql
import datetime
import pandas as pd
import copy

# 定义全局变量
db_connection = pymysql.connect(
    host='123.207.121.89',
    port=3306,
    user='fei',
    password='ddd123',
    database='hd',
    charset='utf8'
    )

h_sql_1 = '''SELECT 
DATE_FORMAT(`通话时间`,'%Y-%m-%d') days,
`任务`, `归属地`,
COUNT(`被叫`) as '外呼',
COUNT(IF(`接通状态`='已接通',TRUE,NULL)) as '接通', 
COUNT(IF(`用户意向`='成功',TRUE,NULL)) as '成功',
CONCAT(ROUND(COUNT(IF(`接通状态`='已接通',TRUE,NULL))/COUNT(`被叫`) * 100 ,1),'%') as '接通率',
CONCAT(ROUND(COUNT(IF(`用户意向`='成功',TRUE,NULL))/COUNT(IF(`接通状态`='已接通',TRUE,NULL)) * 100 ,1),'%') as '成功率',
COUNT(DISTINCT `处理人`) as '坐席',
ROUND(SUM(`通话时长`)/3600 ,1) as 通话时长
FROM `外呼记录`
WHERE `通话时间` 
'''

def ConnectToData(db_connection):
    try:
        cur = db_connection.cursor()
        return cur
    except Exception as e:
        print(e)

def GetData(sql,cursors):
    try:
        cursors.execute(sql)
        results = cursors.fetchall()
        cursors.close()
        return results
    except Exception as e:
        print(e)

end_time = (datetime.datetime.now()+datetime.timedelta(days=1)).strftime('%Y-%m-%d')
start_time = (datetime.datetime.now()+datetime.timedelta(days=-2)).strftime('%Y-%m-%d')
now_time = (datetime.datetime.now()).strftime('%Y-%m-%d %H:%M:%S')

QLSQL = h_sql_1 + '''BETWEEN '%s' AND '%s'
GROUP BY `任务`, `归属地` ,days'''%(start_time,end_time)

QLResult = GetData(QLSQL, ConnectToData(db_connection))


#定义临时变量
a = []
b = []
for i in range(0,len(QLResult)):
    for j in range(0,len(QLResult[i])):
        a.append(QLResult[i][j])
    # 使用深拷贝不影响a改变 同时改变b的尴尬
    b.append(copy.deepcopy(a))
#         print(b)
    a.clear()
#     print(b)
df = pd.DataFrame(b,columns=["日期","任务 刷新时间%s"%now_time, "归属地","外呼量", "接通量","成功量","接通率","成功率","上线人数","通话时长"])
#df.to_html(r"\\Hll\湖北话加\min_data.html")
#os.system(""">> //Hll/湖北话加/min_data.html echo ^<meta http-equiv='refresh' content='10'^>""")
df.to_html(r"min_data.html")
print('''时间段 '%s 00:00:00' AND '%s 00:00:00'已刷新'''%(start_time,end_time))