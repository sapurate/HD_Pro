import time
import datetime

def S_time:
    sql_time = input("默认查询当前时间段成功量（回车），输入l+回车查询上个时间段数据，或手动输入后回车：")
    mon, mday, hour = time.localtime().tm_mon, time.localtime().tm_mday, time.localtime().tm_hour
    if sql_time == "":
        if time.localtime().tm_hour >= 12:
            sql_time = "'2019-%s-%s 12:00:00' AND '2019-%s-%s 23:00:00'"%(mon, mday, mon, mday)
        else:
            sql_time = "'2019-%s-%s 00:00:00' AND '2019-%s-%s 12:00:00'"%(mon, mday, mon, mday)

    if sql_time == "l":
        if time.localtime().tm_hour >= 12:
            sql_time = "'2019-%s-%s 00:00:00' AND '2019-%s-%s 12:00:00'"%(mon, mday, mon, mday)
        else:
            mon = (datetime.datetime.now()+datetime.timedelta(days=-1)).strftime("%m")
            mday = (datetime.datetime.now()+datetime.timedelta(days=-1)).strftime("%d")
            sql_time = "'2019-%s-%s 12:00:00' AND '2019-%s-%s 23:00:00'"%(mon, mday, mon, mday)

    if len(sql_time) == 47:
