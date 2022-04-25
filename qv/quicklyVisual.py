import json
import os

from qv.codes import FLASK_INIT_CODE, FLASK_END_CODE
from qv.dataformats import SQLDataFormat, CSVDataFormat
from qv.htmls import QVHtml
from qv.projects import Page, LinePort, BarPort, PiePort, CloudWord


# 默认以csv模式创建QV
# 也可以使用user host db password参数创建sql模式的QV
# 需要将这四个参数全部填满，不然还是会创建csv模式
def createQV(projectPath, host=None, user=None, password=None, db=None):
    if host is not None and user is not None and password is not None and db is not None:
        dataFormat = SQLDataFormat(host, user, password, db)
    else:
        dataFormat = CSVDataFormat()

    return QuickVisual(projectPath, dataFormat)

# 通过json创建QV
# todo: 未实现完全
# 该方法已被放弃
def createQVByJson(jsonPath):
    js = json.load(open(jsonPath, "r", encoding="utf-8"))

    # 使用指定数据源创建QV
    df = js["dataFormat"]
    if df["flag"] == "sql":
        qv = createQV(js["path"], df["host"], df["user"], df["password"], df["db"])
    if df["flag"] == "csv":
        qv = createQV(js["path"])
    else:
        raise RuntimeError("未知数据源")

    # 添加页面
    for page in js["pages"]:
        qv.addPage(page["page"], page["isIndex"])

        # 添加接口
        for port in page["ports"]:
            if port["type"] == "line":
                if "id" in port:
                    pass
                else:
                    qv.addLinePort(
                        page["page"],
                        port["id"],
                        port["xName"],
                        port["yNames"],
                        port["yDescs"],
                        port["xAxisName"],
                        port["yAxisName"],
                        port["dataSource"]
                    )

            if port["type"] == "bar":
                if "id" in port:
                    pass
                else:
                    pass

            if port["type"] == "pie":
                if "id" in port:
                    pass
                else:
                    pass

            if port["type"] == "wordcloud":
                if "id" in port:
                    pass
                else:
                    pass

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
    def addPortById(self, pageName, id, port, width="400px", height="400px"):
        # todo: 如果存在则忽略，需要修改
        if self.htmls[pageName].isTagExists("div", {"id": port.name}):
            self.pages[pageName].addPort(port)
        else:
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

    #饼图接口
    def addPiePort(self, pageName, name, partName, partDesc, numName, dataSource):
        self.addPort(
            pageName,
            PiePort(
                name,
                partName,
                partDesc,
                numName,
                dataSource
            )
        )

    def addPiePortById(self, pageName, id, name, partName, partDesc, numName, dataSource, width=None, height=None):
        self.addPortById(
            pageName,
            id,
            PiePort(
                name,
                partName,
                partDesc,
                numName,
                dataSource
            ),
            width,
            height
        )

    # 词云图接口
    def addWordCloudPort(self, pageName, name, wordName, numName, dataSource):
        self.addPort(
            pageName,
            CloudWord(
                name,
                wordName,
                numName,
                dataSource
            )
        )

    def addWordCloudPortById(self, pageName, id, name, wordName, numName, dataSource, width=None, height=None):
        self.addPortById(
            pageName,
            id,
            CloudWord(
                name,
                wordName,
                numName,
                dataSource
            ),
            width,
            height
        )

    # 生成对应代码
    def generate(self):

        flaskCode = FLASK_INIT_CODE
        # 选用不同数据输入
        flaskCode += self.dataFormat.generateGetDataCode()

        # 生成代码
        for pageName in self.pages:
            # 如果是主页，则添加主页映射
            if self.pages[pageName].isIndex:
                flaskCode += """@app.route("/")"""

            flaskCode += self.pages[pageName].generateFlaskCode()
            jsCode = ""

            for port in self.pages[pageName].ports:
                flaskCode += port.generateFlaskCode()
                jsCode += port.generatorJSCode()

            # 内嵌JS
            # 如果发现已经存在则删除
            if self.htmls[pageName].isTagExists("script", {"id": "qv-js-src-%s" % pageName}):
                self.htmls[pageName].soup.find("script", {"id": "qv-js-src-%s" % pageName}).decompose()

            self.htmls[pageName].insertTagAfter(
                "script",
                "script",
                content=jsCode,
                newTagAttributes={
                    "id": "qv-js-src-%s" % pageName,
                    "type": "text/javascript",
                    "class": "qv"
                },
                tagAttributes={
                    "id": "qv-echarts-wc-src"
                }
            )

        # 生成flask代码
        with open(self.projectPath + "\\" + "app.py", "w", encoding="utf-8") as f:
            f.write(flaskCode + FLASK_END_CODE)

        # 保存全部HTML代码
        [self.htmls[x].save() for x in self.htmls]

    # 将所有src兼容到static文件夹中
    def __cleanUrl(self, url):
        subUrl = url.replace("..", "")

        while subUrl.startswith("/"):
            subUrl = subUrl[1:]

        if subUrl.startswith('static'):
            subUrl = '/' + subUrl
        else:
            subUrl = '/static/' + subUrl
        return subUrl

    def clean(self):
        for file in os.listdir(self.projectPath + "\\templates"):
            html = QVHtml(self.projectPath + "\\templates\\" + file)

            # 仅修改link script img标签的引用
            for tag in html.iterTags("script"):
                if "src" in tag.attrs and "http" not in tag.attrs["src"]:
                    newTag = html.createTag("script", tag.attrs, tag.string)

                    cleanUrl = self.__cleanUrl(newTag.attrs["src"])
                    if newTag.attrs["src"] == cleanUrl:
                        continue
                    newTag.attrs["src"] = cleanUrl
                    newTag.attrs["class"] = "qv"
                    newTag.attrs["id"] = "qv_org_js_load_%s_%s" % ("scipt", str(abs(hash(tag.prettify()))))
                    tag.insert_after(newTag)
                    html.delTag(tag)

            html.save()

    # 回滚全部页面
    def rollBack(self):
        for file in os.listdir(self.projectPath + "\\templates"):
            html = QVHtml(self.projectPath + "\\templates\\" + file)
            html.rollBack()
            html.save()
