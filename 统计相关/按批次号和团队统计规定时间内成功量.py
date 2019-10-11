import pymysql


def search_success():
    a = input("请输入批次集合：")
    b = a.split(",")
    db = pymysql.connect(host="172.42.28.19", user="hdzf", password="#123zhangf", db="huaplus", port=8066)
    cur = db.cursor()
    for i in b:
        if i:
            batch_id, agent_id = i.split("@")[0], agent[i.split("@")[1]]
            if len(batch_id) != 5:
                print("batch_id位数错误！")
                break
            cur.execute(
                    """SELECT COUNT(called_num) FROM project_record WHERE batch_id =
					%s AND agent_id %s AND end_result = 4 AND ctime BETWEEN %s""" % (batch_id, agent_id, time)
            )
            res = cur.fetchall()
            if res[0][0] != 0:
                print(res[0][0])
            else:
                print("N")

        else:
            print("N")
    db.close()


agent = {"镇江": "= 1238", "嘉鼎": "= 1461815", "中星": "IN ('1461616','1461770')"}
time = "'2019-10-11 12:00:00' AND '2019-10-11 23:00:00'"
search_success()
