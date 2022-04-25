import re

import pymysql

from qe.draw import drawER
from qe.quicklyER import insertDesc, queryDesc, getTables

if __name__ == '__main__':
    connect = pymysql.Connect(host="124.223.43.232", user="root", password="mailbox330.", db="58_house")
    cur = connect.cursor()
    content = ""
    er = {}

    for table in getTables(cur):
        print("生成表： %s 相关数据" % table)
        mdCode = "|字段名|解释|类型|是否允许为空|是否为主键|默认值|\n"

        cur.execute("describe %s" % table)
        rows = cur.fetchall()
        mdCode += "|" + "|".join([":-:" for x in range(len(rows[0]))]) + "|\n"

        tableDesc = queryDesc(table)
        if tableDesc is None:
            tableDesc = input("输入表 '%s' 的解释" % table)
            insertDesc(table, tableDesc)

        er[tableDesc] = []

        columns = []
        descs = []
        for row in rows:

            columns.append(row[0])

            desc = queryDesc(row[0])
            if desc is None:
                desc = input("输入字段 '%s' 的解释" % row[0])
                insertDesc(row[0], desc)
            descs.append(desc)

            isNone = row[2]
            if isNone == "NO":
                isNone = "否"
            else:
                isNone = "是"

            isPrimaryKey = row[3]
            if isPrimaryKey == "PRI":
                isPrimaryKey = "是"
            else:
                isPrimaryKey = "否"

            default = row[4]
            if default is None:
                default = ""

            type = re.sub("\d", "", row[1].replace("(", "").replace(")", ""))
            mdCode += "|" + "|".join([row[0], desc, type, isNone, isPrimaryKey, default]) + "|\n"

            er[tableDesc].append(desc)

        content += "\n\n%s表共有%d个字段,分别是：" % (tableDesc, len(descs)) + "、".join(descs) + "。具体表字段如下表所示:\n\n"
        content += mdCode

    with open("数据库设计.md", 'w', encoding="utf-8") as f:
        f.write(content)

    for entire in er:
        drawER(entire, er[entire])