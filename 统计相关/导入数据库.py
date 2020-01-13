import pymysql, xlrd, sys, os

'''
    连接数据库
    args：db_name（数据库名称）
    returns:db

'''


def mysql_link(db_name):
    try:
        db = pymysql.connect(host="123.207.121.89", user="fei",
                             passwd="ddd123",
                             db=db_name,
                             charset='utf8')
        return db
    except:
        print("could not connect to mysql server")


'''
    读取excel函数
    args：excel_file（excel文件，目录在py文件同目录）
    returns：book
'''


def open_excel(excel_file):
    try:
        book = xlrd.open_workbook(excel_file)  # 文件名，把文件与py文件放在同一目录下
        print(sys.getsizeof(book))
        return book
    except:
        print("open excel file failed!")


'''
    执行插入操作
    args:db_name（数据库名称）
         table_name(表名称）
         excel_file（excel文件名，把文件与py文件放在同一目录下）

'''


def store_to(db_name, table_name, excel_file, city):
    db = mysql_link(db_name)  # 打开数据库连接
    cursor = db.cursor()  # 使用 cursor() 方法创建一个游标对象 cursor

    book = open_excel(excel_file)  # 打开excel文件
    sheets = book.sheet_names()  # 获取所有sheet表名
    for sheet in sheets:
        sh = book.sheet_by_name(sheet)  # 打开每一张表
        row_num = sh.nrows
        print(row_num)
        list = []  # 定义列表用来存放数据
        num = 0  # 用来控制每次插入的数量
        num_max = 0
        for i in range(1, row_num):  # 第一行是标题名，对应表中的字段名所以应该从第二行开始，计算机以0开始计数，所以值是1
            row_data = sh.row_values(i)  # 按行获取excel的值
            value = (row_data[2]+row_data[3],row_data[0], city, row_data[2], row_data[3], row_data[7], row_data[8], row_data[10],
                     row_data[11], row_data[12], row_data[13], row_data[14], row_data[15], row_data[16], row_data[17],
                     row_data[18], row_data[19], row_data[20], row_data[21], row_data[22])
            list.append(value)  # 将数据暂存在列表
            num += 1
            num_max += 1
            if (num >= 10000) or (num_max == row_num - 1):  # 每一万条数据执行一次插入
                print(sys.getsizeof(list))
                sql = "INSERT INTO " + table_name + " (主键, 任务, 归属地, 被叫, 通话时间, 通话时长, 处理人, 接通状态,\
                部门, 用户意向, 外呼备注, 一检结果,一检备注, 二检结果, 二检备注, 沟通结果,产品名称,质检人,二次质检人,呼叫状态)\
                VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                cursor.executemany(sql, list)  # 执行sql语句

                num = 0  # 计数归零
                list.clear()  # 清空list
                print("worksheets: " + sheet + " has been inserted 10000 datas!")

    print("worksheets: " + sheet + " has been inserted " + str(row_num) + " datas!")
    db.commit()  # 提交
    cursor.close()  # 关闭连接
    db.close()


if __name__ == '__main__':
    #遍历目录,注意文件名均为"地市.xlsx"
    path = 'C:/Users/Fei/Desktop/外呼记录/2020-01-13/'
    dirs = os.listdir(path)
    for file in dirs:
        if file in ("荆门.xlsx", "宜昌.xlsx", "江汉.xlsx", "黄冈.xlsx", "襄阳.xlsx",
                    "荆门_本地.xlsx", "宜昌_本地.xlsx", "江汉_本地.xlsx", "黄冈_本地.xlsx", "襄阳_本地.xlsx"):
            store_to('hd', '外呼记录', os.path.join(path, file), file.split(".")[0])
            os.rename(os.path.join(path, file),os.path.join(path, "AM"+file.split(".")[0]+"_已导入."+file.split(".")[1]))
            print(file.split(".")[0]+"=====>已导入")