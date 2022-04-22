import os

from codes import FLASK_INIT_CODE, DATAFRAME_FROM_CSV, DATAFRAME_FROM_MYSQL, FLASK_END_CODE
from config import CONNECTION
from htmlEditor import QVHtml
from projects import Page, LinePort, BarPort

'''
数据格式
'''
class DataFormat:
    # SQL
    SQL = "sql"

    # CSV
    CSV = "csv"


def createQV(projectPath, dataFormat):
    return QuickVisual(projectPath, dataFormat)



class QuickVisual:

    # todo: 输入格式还未实现
    def __init__(self, projectPath, dataFormat):

        # 工程目录
        self.projectPath = projectPath
        if not os.path.exists(projectPath) or not os.path.isdir(projectPath):
            raise RuntimeError("%s 文件夹不存在, 请检查工程目录" % projectPath)
        # 检测工程目录下是否存在templates文件夹和static文件夹
        if not os.path.exists(projectPath + "\\static") or not os.path.isdir(projectPath + "\\static"):
            raise RuntimeError("static文件夹不存在, 请检查工程目录")
        if not os.path.exists(projectPath + "\\templates") or not os.path.isdir(projectPath + "\\templates"):
            raise RuntimeError("templates文件夹不存在, 请检查工程目录")

        # 数据源格式
        self.dataFormat = dataFormat
        # 存储Page类 <页面名称: 页面>
        self.pages = {}
        # 存户qvHtml类 <页面名称: html>
        self.htmls = {}

    # 添加页面
    # 会为页面加载资源
    def addPage(self, pageName, isIndex=False):
        html = QVHtml(self.projectPath + "\\templates\\%s.html" % pageName)
        html.loadResources()
        self.pages[pageName] = Page(pageName, isIndex)
        self.htmls[pageName] = html

    # 添加接口
    def addPort(self, pageName, port):
        self.pages[pageName].addPort(port)

    # 添加接口并修改原ID
    # todo: 重复使用会出现问题
    # todo: 接口普未兼容css
    def addPortById(self, pageName, id, port, width=None, height=None):
        self.pages[pageName].addPort(port)
        self.htmls[pageName].changeDivID(id, port.name, width, height)

    # 折线图接口
    def addLinePort(self, pageName, name, xName, yNames, yDescs, xAxisName, yAxisName, dataSource):
        self.addPort(
            pageName,
            LinePort(
                name,
                xName,
                yNames,
                yDescs,
                xAxisName,
                yAxisName,
                dataSource
            )
        )

    def addLinePortById(self, pageName, id, name, xName, yNames, yDescs, xAxisName, yAxisName, dataSource, width=None,
                        height=None):
        self.addPortById(
            pageName,
            id,
            LinePort(
                name,
                xName,
                yNames,
                yDescs,
                xAxisName,
                yAxisName,
                dataSource,
            ),
            width,
            height
        )

    # 柱状图接口
    def addBarPort(self, pageName, name, xName, yNames, yDescs, xAxisName, yAxisName, dataSource):
        self.addPort(
            pageName,
            BarPort(
                name,
                xName,
                yNames,
                yDescs,
                xAxisName,
                yAxisName,
                dataSource
            )
        )

    def addBarPortById(self, pageName, id, name, xName, yNames, yDescs, xAxisName, yAxisName, dataSource, width=None,
                       height=None):
        self.addPortById(
            pageName,
            id,
            BarPort(
                name,
                xName,
                yNames,
                yDescs,
                xAxisName,
                yAxisName,
                dataSource
            ),
            width,
            height
        )

    # 生成对应代码
    def generate(self):

        # 检查qv文件夹是否存在, 不存在则创建
        if not os.path.exists(self.projectPath + "\\static\\qv"):
            os.mkdir(self.projectPath + "\\static\\qv")

        # 选用不同数据输入
        flaskCode = FLASK_INIT_CODE
        if self.dataFormat == DataFormat.CSV:
            flaskCode += DATAFRAME_FROM_CSV
        else:
            flaskCode += DATAFRAME_FROM_MYSQL % CONNECTION

        # 生成代码
        for pageName in self.pages:
            flaskCode += self.pages[pageName].generateFlaskCode()
            jsCode = ""

            for port in self.pages[pageName].ports:
                flaskCode += port.generateFlaskCode()
                jsCode += port.generatorJSCode()

            # 创建每个page对应的js文件
            with open(self.projectPath + "\\static\\qv\\%s.js" % pageName, "w", encoding="utf-8") as f:
                f.write(jsCode)

            # 将创建的js文件引入对应页面
            self.htmls[pageName].loadJS(pageName)

        # 生成flask代码
        with open(self.projectPath + "\\" + "qv.py", "w", encoding="utf-8") as f:
            f.write(flaskCode + FLASK_END_CODE)

        # 保存全部HTML代码
        [self.htmls[x].save() for x in self.htmls]

    # 回滚全部页面
    def rollBack(self):
        for file in os.listdir(self.projectPath + "\\templates"):
            html = QVHtml(self.projectPath + "\\templates\\" + file)
            html.rollBack()
            html.save()

