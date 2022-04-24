import re

import os
from models import *
from qv.codes import *


def printWithSchema(content):
    print("[*] " + content)


# 将添加static前缀
def clean1():
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

def clean():
    printWithSchema("start clean")
    for file in os.listdir(ROOT_PATH + "\\templates"):
        path = ROOT_PATH + "\\templates\\"
        content = ""
        with open(path + file, "r", encoding="utf-8") as f:
            content = f.read()
        srcs = [x[1] for x in re.findall(r'(src|href)="(.*?\.(css|js|jpg|png|img))"', content)]
        srcs = list(filter(lambda x: not x.startswith("http"), srcs))

        for url in srcs:
            subUrl = url.replace("..", "")

            while subUrl.startswith("/"):
                subUrl = subUrl[1:]

            if subUrl.startswith('static'):
                subUrl = '/' + subUrl
            else:
                subUrl = '/static/' + subUrl

            printWithSchema("find broken url:%s" % url)
            content = content.replace(url, subUrl)

        with open(path + file, "w", encoding="utf-8") as f:
            f.write(content)

    printWithSchema("end clean")

def dropHref():
    printWithSchema("start drop href")

    if not input("使用此函数会使所有a标签无法跳转，输入任意值继续，输入exit退出").strip() == "exit":
        for file in os.listdir(ROOT_PATH + "\\templates"):
            html = BeautifulSoup(open(ROOT_PATH + "\\templates\\%s" % file, encoding="utf-8"), "html.parser")
            for href in html.find_all("a"):
                if 'href' in href.attrs and href.attrs['href'] != "#":
                    printWithSchema("drop a tag's href % s" % href.attrs['href'])
                    href.attrs['href'] = "#"
            with open(ROOT_PATH + "\\templates\\%s" % file, "w", encoding="utf-8") as f:
                f.write(html.prettify())

    printWithSchema("drop href done")


class QuickVisual():

    def __init__(self, dataFrameFromCSV=True):
        printWithSchema("start QuickVisual...")

        if not os.path.exists(ROOT_PATH + "\\static\\qv"):
            printWithSchema("create resource directory: %s" % ROOT_PATH + "\\static\\qv")
            os.mkdir(ROOT_PATH + "\\static\\qv")

        printWithSchema("create jquery-3.3.1.min.js and echarts.js")
        with open(ROOT_PATH + "\\static\\qv\\jquery-3.3.1.min.js", "w", encoding="utf-8") as f, open("resource\\jquery-3.3.1.min.js", "r", encoding="utf-8") as jq:
            f.write(jq.read())

        self.dataFrameFromCSV = dataFrameFromCSV
        self.pages = []

    def addPage(self, page):
        self.pages.append(page)

    def generate(self):

        flaskCode = FLASK_INIT_CODE
        if self.dataFrameFromCSV:
            printWithSchema("enable data from csv")
            flaskCode += DATAFRAME_FROM_CSV
        else:
            # flaskCode += CONNECTION
            flaskCode += DATAFRAME_FROM_MYSQL % CONNECTION
            printWithSchema("enable data from mysql")
            printWithSchema("your mysql setting is %s" % CONNECTION.replace("\n", "").replace(" ", ""))

        for page in self.pages:
            printWithSchema("create page %s" % page.name)

            flaskCode += page.generateFlaskCode()
            jsCode = ""
            cssCode = ""

            for port in page.ports:
                printWithSchema("create chart port: %s" % port.name)
                flaskCode += port.generateFlaskCode()
                jsCode += port.generatorJSCode()
                cssCode += PORT_CSS_CODE % port.name

            with open(ROOT_PATH + "\\static\\qv\\%s.js" % page.name, "w", encoding="utf-8") as f:
                f.write(jsCode)
            with open(ROOT_PATH + "\\static\\qv\\%s.css" % page.name, "w", encoding="utf-8") as f:
                f.write(cssCode)

        with open(ROOT_PATH + "\\" + "qv.py", "w", encoding="utf-8") as f:
            f.write(flaskCode + FLASK_END_CODE)

        printWithSchema("done !")
