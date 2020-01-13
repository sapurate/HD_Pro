batch_dict = {
    "江汉-超级会员": "'36978','36979','37227','37228'",
    "江汉-套餐迁转": "'37215','37219'",
    "江汉-流量包": "'37187','37210','37226','37232'",
    "江汉-低消": "'37101','37186'",
    "江汉-非办理类": "'36402','36983'",
    "荆门-超级会员": "'37014','37200','37211','37224'",
    "荆门-套餐迁转": "'37193','37194','37195','37205'",
    "荆门-流量包": "'37182','37192','37196','37203','37225'",
    "荆门-低消": "'37020','37207','37214'",
    "荆门-非办理类": "'36941','37158'",
    "襄阳-超级会员": "'37039','37041','37042','37046','37179','37180','37213'",
    "襄阳-套餐迁转": "'37188','37204'",
    "襄阳-流量包": "'37030','37171'",
    "宜昌-超级会员": "'36959','37049','37173','37174','37175','37176','37177','37212','37223','37231','37233'",
    "宜昌-套餐迁转": "'36949','36992','37142','37198','37199','37208','37209','37222'",
    "宜昌-流量包": "'37220','37229','37230'",
    "宜昌-低消": "'37183'",
    "宜昌-非办理类": "'37201','37217'"
}

sheel_dict = {
    "超级会员": "8",
    "套餐迁转": "11",
    "流量包": "17",
    "低消": "14",
    "非办理类": "20",

}



import pymysql, openpyxl

def do_it(now_time):
    ctime = "'%s 00:00:00' AND '%s 23:00:00'" % (now_time, now_time)

    wb = openpyxl.load_workbook(r"C:\Users\Fei\Desktop\报表\对内\2019-12\%s.xlsx" % now_time)
    db = pymysql.connect(host="172.42.28.19", user="hdzf", password="#123zhangf", db="huaplus", port=8066)
    cur = db.cursor()

    for i in batch_dict:
        city, biz = i.split("-")[0], i.split("-")[1]
        cell = sheel_dict[biz]
        ws = wb[city]
        cur.execute("""SELECT COUNT(called_num),COUNT(IF(call_duration > 0,true,null)),COUNT(IF(end_result=4,true,null))
        FROM project_record WHERE batch_id IN (%s) AND ctime BETWEEN %s""" % (batch_dict[i], ctime))
        res = cur.fetchall()
        ws['F%s'%cell] = res[0][0]
        ws['G%s'%cell] = res[0][1]
        ws['J%s'%cell] = res[0][2]
        print(i, now_time, "====>ok")
    wb.save(r"C:\Users\Fei\Desktop\报表\对内\2019-12\%s.xlsx" % now_time)

for num in range (10,32):
    now_time = "2019-12-%s"%num
    do_it(now_time)