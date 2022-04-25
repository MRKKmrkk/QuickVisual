import re
import time

import pymysql
import requests
import hashlib

from qe.draw import drawER
from qe.models import Table


def getTables(cur):
    cur.execute("show tables")
    return [x[0] for x in cur.fetchall()]


def queryDesc(fieldName):
    res = requests.post("http://124.223.43.232:9653/query", data={"field": fieldName})

    if res.status_code != 200:
        return None

    return res.text

def insertDesc(fieldName, desc):
    requests.post("http://124.223.43.232:9653/insert", data={"field": fieldName, "desc": desc})

def updateDesc(fieldName, desc):
    requests.post("http://124.223.43.232:9653/update", data={"field": fieldName, "desc": desc})

def qeGenerateInfoDoc(host, user, password, db):
    connect = pymysql.Connect(host=host, user=user, password=password, db=db)
    cur = connect.cursor()

    tables = []

    for tableName in getTables(cur):

        tableDesc = queryDesc(tableName)
        if tableDesc is None:
            tableDesc = input("输入表 '%s' 的解释" % tableName)
            insertDesc(tableName, tableDesc)

        table = Table(tableName, tableDesc)

        cur.execute("describe %s" % table.tableName)
        for row in cur.fetchall():

            columnDesc = queryDesc(row[0])
            if columnDesc is None:
                columnDesc = input("输入字段 '%s' 的解释" % row[0])
                insertDesc(row[0], columnDesc)

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

            table.addColumn(
                row[0],
                columnDesc,
                re.sub("\d", "", row[1].replace("(", "").replace(")", "")),
                isNone,
                isPrimaryKey,
                default
            )
        tables.append(table)

    content = ""
    for table in tables:
        content += table.getTableInfoDoc()

    with open("info", "w", encoding="utf-8") as f:
        f.write(content)

def parseInfoDoc():
    with open("info", "r", encoding="utf-8") as f:
        content = f.read()
        tables = []
        mdCode = ""

        for tableContent in content.strip().split("==============\n"):
            fields = re.findall("=([^=]*?)\:(.*?)=", tableContent)

            table = Table(fields[0][0], fields[0][1])
            for col in tableContent.strip().split("\n")[1:]:
                if col.startswith("="):
                    continue

                cols = col.split(",")
                table.addColumn(
                    cols[0],
                    cols[1],
                    cols[2],
                    cols[3],
                    cols[4],
                    cols[5],
                )
            tables.append(table)

            mdCode += table.generateMarkDownCode()

        with open("数据库设计.md", "w", encoding="utf-8") as f:
            f.write(mdCode)

    time.sleep(1)
    for table in tables:
        drawER(table.tableDesc, table.getDescs())


if __name__ == '__main__':
    # qeGenerateInfoDoc("", "", "", "")
    parseInfoDoc()