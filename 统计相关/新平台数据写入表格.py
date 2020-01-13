batch_dict = (
            "江汉-超级会员","江汉-套餐迁转","江汉-流量包","江汉-低消","江汉-非办理类",
            "荆门-超级会员","荆门-套餐迁转","荆门-流量包","荆门-低消","荆门-非办理类",
            "襄阳-超级会员","襄阳-套餐迁转","襄阳-流量包","襄阳-低消","襄阳-非办理类",
            "宜昌-超级会员","宜昌-套餐迁转","宜昌-流量包","宜昌-低消","宜昌-非办理类"
            )

sheel_lo_dict = {
    "超级会员": "8",
    "套餐迁转": "11",
    "流量包": "17",
    "低消": "14",
    "非办理类": "20",

}
sheel_dict = {
    "超级会员": "7",
    "套餐迁转": "10",
    "流量包": "16",
    "低消": "13",
    "非办理类": "19",

}



import pymysql, openpyxl

def do_it(now_time):
    ctime = "'%s 00:00:00' AND '%s 23:00:00'" % (now_time, now_time)
    wb = openpyxl.load_workbook(r"C:\Users\Fei\Desktop\报表\对内\2020-01\%s.xlsx" % now_time)
    db = pymysql.connect(host="123.207.121.89", user="fei",passwd="ddd123",db="hd",charset='utf8')
    cur = db.cursor()
    for i in batch_dict:
        city, biz = i.split("-")[0], i.split("-")[1]
        cell = sheel_dict[biz]
        ws = wb[city]
        cur.execute("""SELECT 
        COUNT(`被叫`) as '外呼',
        COUNT(IF(`接通状态`='已接通',TRUE,NULL)) as '接通', 
        COUNT(IF(`用户意向`='成功',TRUE,NULL)) as '成功'
        FROM `外呼记录`
        WHERE `通话时间` LIKE '%s%'
        AND `处理人` IN ("徐丽丽","宋康怡","丁慧娟","陈云")
        AND `任务` IN (SELECT `任务` FROM `202001项目` WHERE `一级项目类型` = '%s' AND `地市` = '%s') """ % (ctime,biz,city))
        res = cur.fetchall()
        ws['F%s'%cell] = res[0][0]
        ws['G%s'%cell] = res[0][1]
        ws['J%s'%cell] = res[0][2]
        print(i, now_time, "====>ok")
    wb.save(r"C:\Users\Fei\Desktop\报表\对内\2020-01\%s.xlsx" % now_time)

for num in range (2,6):
    now_time = "2020-01-0%s"%num
    do_it(now_time)