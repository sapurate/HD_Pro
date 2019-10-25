from wheel import search_sql, update_sql
uid = search_sql("SELECT id FROM user WHERE username = '%s' LIMIT 1"%input("请输入坐席账号："))
print("查询得到uid为：%s"%uid[0])