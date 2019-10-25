def search_sql (sql) :
    import pymysql
    db = pymysql.connect(host="172.42.28.19", user="hdzf", password="#123zhangf", db="huaplus", port=8066)
    cur = db.cursor()
    cur.execute(sql)
    res = cur.fetchall()
    db.close()
    return res

def update_sql (sql) :
    import pymysql
    db = pymysql.connect(host="172.42.28.15", user="hdzf", password="#123zhangf", db="huaplus", port=8066)
    cur = db.cursor()
    res = cur.execute(sql)
    db.close()
    return res

if __name__ == '__main__':
    print("我是个轮子，我只能被引用！")
