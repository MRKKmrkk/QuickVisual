import json
import os
import re

from mqv.projects import *
from mqv.dataformats import *
from mqv.codes import *
from mqv.util import concatPath, concatPaths
from mqv.htmls import *

# 默认以csv模式创建QV
# 也可以使用user host db password参数创建sql模式的QV
# 需要将这四个参数全部填满，不然还是会创建csv模式
def createMQV(modelPath, projectPath, host=None, user=None, password=None, db=None):
    if host is not None and user is not None and password is not None and db is not None:
        dataFormat = SQLDataFormat(host, user, password, db)
    else:           
        dataFormat = CSVDataFormat()

    return ModelQuicklyVisual(modelPath, projectPath, dataFormat)

class ModelQuicklyVisual:

    def __init__(self, modelPath, projectPath, dataFormat):
        self.modelPath = modelPath
        self.projectPath = projectPath
        self.dataFormat = dataFormat
        self.indexPage = Page("index", True) 
        self.indexHtml = QVHtml(modelPath, concatPaths(projectPath, "templates", "index.html"))

        # 工程目录
        self.projectPath = projectPath
        if not os.path.exists(projectPath) or not os.path.isdir(projectPath):
            raise RuntimeError("%s 文件夹不存在, 请检查工程目录" % projectPath)
        # 检测工程目录下是否存在templates文件夹和static文件夹
        if not os.path.exists(concatPath(projectPath, "static")) or not os.path.isdir(concatPath(projectPath, "static")):
            raise RuntimeError("static文件夹不存在, 请检查工程目录")
        if not os.path.exists(concatPath(projectPath, "templates")) or not os.path.isdir(concatPath(projectPath, "templates")):
            raise RuntimeError("templates文件夹不存在, 请检查工程目录")

        # 验证模板
        #if not self.indexHtml.isTagExists(None, attributes={"id": "qv-js-src-index"}):
        #    raise RuntimeError("非可用模板，请检查模板文件1")
        if not self.indexHtml.isTagExists(None, attributes={"side-bar-model": "true"}):
            raise RuntimeError("非可用模板，请检查模板文件2")

 
    # 添加接口
    def addPort(self, port):                                                                      
        self.indexPage.addPort(port)

    # 折线图接口
    def addLinePort(self, name, desc, xName, yNames, yDescs, xAxisName, yAxisName, dataSource):
        self.addPort(
            LinePort(
                name,
                desc,
                xName,
                yNames,
                yDescs,
                xAxisName,
                yAxisName,
                dataSource
            )
        )

    # 柱状图接口
    def addBarPort(self, name, desc, xName, yNames, yDescs, xAxisName, yAxisName, dataSource):
        self.addPort(
            BarPort(
                name,
                desc,
                xName,
                yNames,
                yDescs,
                xAxisName,
                yAxisName,
                dataSource
            )
        )

    #饼图接口
    def addPiePort(self, name, desc, partName, partDesc, numName, dataSource):
        self.addPort(
            PiePort(
                name,
                desc,
                partName,
                partDesc,
                numName,
                dataSource
            )
        )

    # 词云图接口
    def addWordCloudPort(self, name, desc, wordName, numName, dataSource):
        self.addPort(
            CloudWord(
                name,
                desc,
                wordName,
                numName,
                dataSource
            )
        )

    def _cleanTag(self, content):
        s = 0
        while (content[s] != ">"):
            s += 1

        e = len(content) - 1
        while (content[e] != "<"):
            e -= 1

        return content[s + 1: e]


    def generate(self):                                                                                        
        flaskCode = FLASK_INIT_CODE
        # 选用不同数据输入
        flaskCode += self.dataFormat.generateGetDataCode()

        # 生成代码
        #添加主页映射
        flaskCode += """@app.route("/")"""
        flaskCode += self.indexPage.generateFlaskCode()
        jsCode = ""

        # 侧边栏模板读取
        sideBar = self.indexHtml.soup.find(None, attrs={"side-bar-model": "true"})
        sideBarName = sideBar.name
        sideBarAttrs = {}
        
        sideBarInsideTags = sideBar.prettify().replace("\n", "")
        #sideBarInsideTags = re.findall(r"^<%s.*?>(.*?)<.*?%s>$" % (sideBarName, sideBarName), sideBarInsideTags)[0] 
        sideBarInsideTags = self._cleanTag(sideBarInsideTags)


        for i in sideBar.attrs:
            if not (i == "side-bar-model" or i == "id"):
                sideBarAttrs[i] = sideBar.attrs[i]

        for port in self.indexPage.ports:
            flaskCode += port.generateFlaskCode()
            jsCode += port.generatorJSCode()

            #todo: 生成侧边栏
            curTag = self.indexHtml.soup.new_tag(sideBarName, attrs=sideBarAttrs)
            curTag.attrs["id"] = port.name
            curTag.insert(1, BeautifulSoup(sideBarInsideTags.replace("qv-side-bar-model-content", port.desc), "html.parser"))
            sideBar.insert_after(curTag)

        # 内嵌JS
        self.indexHtml.insertTagIn(
            "body",
            "script",
            -1, 
            content=jsCode,
            newTagAttributes={
                "id": "qv-js-src-index",
                "type": "text/javascript",
            }   
        )   


        # 生成html
        self.indexHtml.save()
        # 生成flask代码
        with open(concatPath(self.projectPath, "app.py"), "w", encoding="utf-8") as f:
            f.write(flaskCode + FLASK_END_CODE)





