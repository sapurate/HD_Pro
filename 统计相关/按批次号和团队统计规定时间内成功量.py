import pymysql
import time
import datetime
import os
from openpyxl import Workbook

def search_m_success():
	a = input("请输入批次集合：时间段为%s"%SN_time)
	b = a.split(",")
	wb = Workbook()
	ws = wb.active
	db = pymysql.connect(host="172.42.28.19", user="hdzf", password="#123zhangf", db="huaplus", port=8066)
	cur = db.cursor()
	for i in b:
		if i:
			batch_id, agent_id = i.split("@")[0], agent[i.split("@")[1]]
			if len(batch_id) != 5:
				print("batch_id位数错误！")
				break
			cur.execute("""SELECT COUNT(called_num),COUNT(IF(call_duration > 0,true,null)),COUNT(IF(end_result=4,true,null))
FROM project_record WHERE batch_id = %s AND agent_id %s AND ctime %s"""%(batch_id,agent_id,SN_time))
			res = cur.fetchall()
			if res[0][2] != 0:
				ws.append([batch_id, i.split("@")[1], res[0][0], res[0][1], res[0][2]])
			else:
				ws.append([batch_id, i.split("@")[1], "N", "N", "N"])
		else:
			ws.append(["", "", "","", "N"])
	wb.save("C:\\Users\\Administrator\\Desktop\\sample.xlsx")
	print("Done.")
	db.close()
    os.startfile("C:\\Users\\Administrator\\Desktop\\sample.xlsx")


def search_success():
	a = input("请输入批次集合：时间段为%s"%SN_time)
	b = a.split(",")
	db = pymysql.connect(host="172.42.28.19", user="hdzf", password="#123zhangf", db="huaplus", port=8066)
	cur = db.cursor()
	num = 0
	for i in b:
		if i:
			batch_id, agent_id = i.split("@")[0], agent[i.split("@")[1]]
			if len(batch_id) != 5:
				print("batch_id位数错误！")
				break
			cur.execute(
					"""SELECT COUNT(called_num) FROM project_record WHERE batch_id =
					%s AND agent_id %s AND end_result = 4 AND ctime BETWEEN %s""" % (batch_id, agent_id, SN_time)
			)
			res = cur.fetchall()
			if res[0][0] != 0:
				print("#"+str(res[0][0]))
				num = num + 1
			else:
				print("N")

		else:
			print("N")
	print("共有项目%d"%num)
	db.close()

def S_time():
	sql_time = input("默认查询当前时间段成功量（回车），输入l+回车\m+回车查询上个时间段\当月数据，或手动输入后回车：")
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

	if sql_time == "m":
			sql_time = "BETWEEN '2019-%s-01 00:00:00' AND '2019-%s-%s 23:00:00'"%(mon, mon, mday)
	return  sql_time

agent = {"镇江": "= 1238", "嘉鼎": "= 1461815", "中星": "IN ('1461616','1461770')"}
SN_time = S_time()

if len(SN_time) == 47:
	search_success()
if len(SN_time) > 47:
	search_m_success()
