import re

from config import *
import os
from models import *
from codes import *


def printWithSchema(content):
    print("[*] " + content)


# 将添加static前缀
def clean():
    printWithSchema("start clean")
    for file in os.listdir(ROOT_PATH + "\\templates"):
        path = ROOT_PATH + "\\templates\\"
        content = ""
        with open(path + file, "r", encoding="utf-8") as f:
            content = f.read()
        srcs = [x[1] for x in re.findall(r'(src|href)="(.*?\.(css|js))"', content)]
        srcs = list(filter(lambda x: not x.startswith("http"), srcs))

        for url in srcs:
            if url.startswith("/static") or url.startswith("static"):
                continue

            printWithSchema("find broken url:%s" % url)
            if url.startswith("/"):
                content = content.replace(url, "/static" + url)
            else:
                content = content.replace(url, "/static/" + url)

        with open(path + file, "w", encoding="utf-8") as f:
            f.write(content)
    printWithSchema("end clean")


class QuickVisual():

    def __init__(self, dataFrameFromCSV=True):
        if not os.path.exists(ROOT_PATH + "\\static\\qv"):
            os.mkdir(ROOT_PATH + "\\static\\qv")
        with open(ROOT_PATH + "\\static\\qv\\jquery-3.3.1.min.js", "w", encoding="utf-8") as f, open("resource\\jquery-3.3.1.min.js", "r", encoding="utf-8") as jq:
            f.write(jq.read())
        with open(ROOT_PATH + "\\static\\qv\\echarts.js", "w", encoding="utf-8") as f, open("resource\\echarts.js", "r", encoding="utf-8") as ec:
            f.write(ec.read())

        self.dataFrameFromCSV = True
        self.pages = []

    def addPage(self, page):
        self.pages.append(page)

    def generate(self):

        flaskCode = FLASK_INIT_CODE
        if self.dataFrameFromCSV:
            flaskCode += DATAFRAME_FROM_CSV
        else:
            flaskCode += DATAFRAME_FROM_MYSQL

        for page in self.pages:
            flaskCode += page.generateFlaskCode()
            jsCode = ""

            for port in page.ports:
                flaskCode += port.generateFlaskCode()
                jsCode += port.generatorJSCode()
            with open(ROOT_PATH + "\\static\\qv\\%s.js" % page.name, "w", encoding="utf-8") as f:
                f.write(jsCode)

        with open(ROOT_PATH + "\\" + "qv.py", "w", encoding="utf-8") as f:
            f.write(flaskCode + FLASK_END_CODE)
