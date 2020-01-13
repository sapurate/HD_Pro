# -*- coding:utf-8 -*-
'''
实现分归属项目类型的报表全月统计
file_path:报表存放的路径
process_table:月项目外呼进度协作表
'''
import os, pymysql, openpyxl, time

# 定义数据库连接属性全局变量
db_connection = pymysql.connect(
    host='123.207.121.89',
    port=3306,
    user='fei',
    password='ddd123',
    database='hd',
    charset='utf8'
)
# 定义读、写报表存放的路径及表名
file_path = r"D:\Data\report"
process_table = r"D:\Data\report\process_table.xlsx"

# 从日进度表中获得：
'''
归属-项目类型 字典：
归属-项目类型-日开户量 字典
'''


def Get_From_Process_Table():
    find_items = ['地市', '类型', '项目', '01', '表尾']  # 定位，表头：地市、类型、及第一天；表尾
    items_location = dict.fromkeys(find_items)
    wb = openpyxl.load_workbook(process_table.replace('\\', '/'))
    ws = wb[wb.sheetnames[0]]
    for i in range(1, ws.max_row + 1):
        for j in range(1, ws.max_column + 1):
            if ws.cell(i, j).value in find_items:
                items_location[ws.cell(i, j).value] = [i, j]
    col_city = items_location[find_items[0]][1]  # 地市列
    col_item = items_location[find_items[1]][1]  # 项目类型列
    col_project = items_location[find_items[2]][1]  # 项目列
    col_day01 = items_location[find_items[3]][1]  # 日开始第一天的列
    row_max = items_location[find_items[4]][0]
    if row_max > 1:
        city_item_postion = {}
        city_item_project = {}
        for i_row in range(2, row_max):
            city = ws.cell(i_row, col_city).value
            item = ws.cell(i_row, col_item).value
            project = ws.cell(i_row, col_project).value
            if city and item:
                city_item_postion.setdefault(city + '-' + item, []).append(i_row)
                city_item_project.setdefault(city + '-' + item, []).append(project)
    print(city_item_postion)
    print(city_item_project)
    # 计算日开单量
    city_item_day_order = {}
    for city_item, postion in city_item_postion.items():
        for d in range(1, 32):
            day_orders = 0  # 当天所有同类型项目开单和
            day_order_s = 0  # 某一类型项目某天上午开单，计算不同天时就行归零操作
            day_order_x = 0  # 某一类型项目某天下午开单，计算不同天时就行归零操作
            for item_col in range(0, len(postion)):
                day_order_s = ws.cell(postion[item_col], col_day01 + (d - 1) * 2).value
                day_order_x = ws.cell(postion[item_col], 1 + col_day01 + (d - 1) * 2).value
                if day_order_s:
                    if '#' not in str(day_order_s):
                        day_orders = day_orders + int(day_order_s)
                if day_order_x:
                    if '#' not in str(day_order_x):
                        day_orders = day_orders + int(day_order_x)
            if d < 10:
                D = '2020-01-0' + str(d)  # 根据统计年限可改
            else:
                D = '2020-01-' + str(d)
            city_item_day_order.setdefault(city_item, {})[D] = day_orders
    #     print(city_item_day_order)
    return (city_item_day_order, city_item_postion, city_item_project)


# 定义数据库连接函数，返回连接游标
def ConnectToData(db_connection):
    try:
        cur = db_connection.cursor()
        return cur
    except Exception as e:
        print(e)


# 传入sql语句字符串，及连接游标
def GetData(sql, cursors):
    try:
        cursors.execute(sql)
        results = cursors.fetchall()
    except Exception as e:
        print(e)
    return results  # 返回查询结果


# 新建Excel,并创建表头,传入文件夹路径，表名，sheet名，批次;返回wb对象
def CreateWb(filepath, wbname, sheetname, headoftable):
    # 表名存在就创建，存在就跳过
    path = os.path.join(filepath + "\\" + wbname + ".xlsx")
    p1 = os.path.exists(path)
    if p1:
        pass  # 如果存在就不管
    else:  # 如果不存在就创建
        wb = openpyxl.Workbook()
        wb.save(filename=path.replace('\\', '/'))
    # 获得已存在表的对象wb
    wb = openpyxl.load_workbook(filename=path.replace('\\', '/'))
    # 根据表名sheetname，删除旧表，创建新表
    if sheetname in wb.sheetnames:
        del wb[sheetname]  # 删除旧表,目前只能用del,remove还不行
        ws = wb.create_sheet(sheetname)  # 新建空表，得到表对象ws
    else:
        ws = wb.create_sheet(sheetname)  # 新建空表，得到表对象ws
    # 准备表头
    # 数据写入是按照1,1的方式 range 计数是0、1、2....6,并初始化为0
    for i in range(len(headoftable)):
        ws.cell(row=1, column=i + 1).value = headoftable[i]
    wb.save(filename=path.replace('\\', '/'))
    return wb, ws  # 返回可操作的对象: 整个工作簿wb,相应工作表ws


# 查询结果并将结果写入到表
def save_result(sheetname, projectnames, outfilepath, city_item_day_order):
    wbname = sheetname.split("-")[0]
    out_fileName = os.path.join(outfilepath + "\\" + wbname + ".xlsx")
    # 准备表头
    headoftable = ["外呼日期", "日外呼量", "日接通量", "日成功量", "日外呼坐席数", "开户量"]
    # 准备表
    (wb, ws) = CreateWb(outfilepath, wbname, sheetname, headoftable)
    str_pro = "("
    for i in range(0, len(projectnames)):
        if i != len(projectnames) - 1:
            str_pro = str_pro + "'" + projectnames[i] + "',"
        else:
            str_pro = str_pro + "'" + projectnames[i] + "')"
    # 查询字符串构造
    QLSQL = '''SELECT DATE_FORMAT(通话时间, '%%Y-%%m-%%d') days,
               count(被叫)  as "外呼量",COUNT(IF(通话时长 > 0,true,null)) as "接通量",COUNT(DISTINCT IF(用户意向="成功",被叫,null)) as "成功量",
               count(DISTINCT 处理人)  as "外呼坐席数"
               FROM 外呼记录  where 任务 in %s GROUP BY days''' % str_pro

    cur = ConnectToData(db_connection)
    QLResult = GetData(QLSQL, cur)

    #     print(QLSQL)
    #     print(QLResult)
    # 结果写入表格
    for r in range(0, len(QLResult)):
        for c in range(0, len(QLResult[r])):
            # 从第二行第二列开始写入,构造小表，统计总外呼情况
            ws.cell(row=r + 2, column=c + 1).value = QLResult[r][c]
            if c == len(QLResult[r]) - 1:
                ws.cell(row=r + 2, column=c + 2).value = city_item_day_order[sheetname][QLResult[r][0]]
    wb.save(filename=out_fileName.replace('\\', '/'))


if __name__ == '__main__':
    Get_From_Process_Table()
    (city_item_day_order, city_item_postion, city_item_project) = Get_From_Process_Table()
    for key, value in city_item_project.items():  # 遍历字典
        try:
            save_result(key, value, file_path, city_item_day_order)
            print(key + "==>" + "成功统计")
            time.sleep(1)
        except Exception as e:
            print(e)
    db_connection.close()  # 查完即关闭
