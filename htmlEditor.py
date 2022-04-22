from bs4 import BeautifulSoup

'''
冲突模式
'''
class ConflictMode:
    # 覆盖
    OVERWRITE = "overwrite"

    # 忽略 会导致两个冲突共存
    IGNORE = "ignore"

    # 保持原有引用
    KEEP = "keep"


'''
HTML类支持对Html的编辑操作
'''
class HTML:

    def __init__(self, path, encoding="utf-8"):
        self.path = path
        self.encoding = encoding
        self.soup = BeautifulSoup(open(path, encoding=encoding), "html.parser")

    # 查询标签是否存在
    def isTagExists(self, tagName, attributes={}):
        return len(self.soup.find_all(tagName, attrs=attributes)) > 0

    # 向指定元素内增加一个子元素
    # 运行此方法后需要执行save() 方法才能保存
    def insertTagIn(self, tagName, newTagName, index, content="", tagAttributes={}, newTagAttributes={}):
        newTag = self.soup.new_tag(newTagName, attrs=newTagAttributes)
        newTag.string = content
        self.soup.find(tagName, attrs=tagAttributes).insert(index, newTag)

    # 向指定元素后插入元素
    def insertTagAfter(self, tagName, newTagName, content="", tagAttributes={}, newTagAttributes={}):
        newTag = self.soup.new_tag(newTagName, attrs=newTagAttributes)
        newTag.string = content
        self.soup.find(tagName, attrs=tagAttributes).insert_after(newTag)

    # 向指定元素前插入元素
    def insertTagBefore(self, tagName, newTagName, content="", tagAttributes={}, newTagAttributes={}):
        newTag = self.soup.new_tag(newTagName, attrs=newTagAttributes)
        newTag.string = content
        self.soup.find(tagName, attrs=tagAttributes).insert_before(newTag)

    # 修改指定标签元素的内容
    def alterTagContent(self, tagName, content, attributes={}):
        tag = self.soup.find(tagName, attrs=attributes)
        tag.string = content

    # 修改指定标签的属性
    def alertTagAttrs(self, tagName, attributes, newAttributes):
        tag = self.soup.find(tagName, attrs=attributes)
        tag.attrs = newAttributes

    # 删除指定标签
    def delTag(self, tagName, attributes={}):
        [x.decompose() for x in self.soup.find_all(tagName, attrs=attributes)]

    # 保存html文件
    def save(self):
        with open(self.path, "w", encoding="utf-8") as f:
            f.write(self.soup.prettify())

    # 遍历指定元素
    def iterTags(self, name=None, attributes={}):
        for tag in self.soup.find_all(name, attrs=attributes):
            yield tag


'''
基于QV业务的HTML编辑功能
'''
class QVHtml(HTML):

    def __init__(self, path, conflictMode=ConflictMode.OVERWRITE):
        self.conflictMode = conflictMode
        super(QVHtml, self).__init__(path)

    # 在body标签的末尾
    # 添加jquery引用
    # 如已经添加则忽略
    def addJquery(self):
        if self.isTagExists("script", attributes={"id": "qv-jquery-src"}):
            return

        self.insertTagIn(
            "body",
            "script",
            -1,
            newTagAttributes={
                "class": "qv",
                "id": "qv-jquery-src",
                "type": "text/javascript",
                "src": "https://cdn.bootcss.com/jquery/3.3.1/jquery.min.js"
            }
        )

    # 加入Echarts依赖
    # 必须先加入JQuery依赖
    # 如已经添加则忽略
    def addECharts(self):
        if self.isTagExists("script", attributes={"id": "qv-echarts-src"}):
            return

        if not super(QVHtml, self).isTagExists("script", {"id": "qv-jquery-src"}):
            raise RuntimeError("需要先导入JQuery依赖")

        self.insertTagAfter(
            "script",
            "script",
            tagAttributes={"id": "qv-jquery-src"},
            newTagAttributes={
                "class": "qv",
                "id": "qv-echarts-src",
                "type": "text/javascript",
                "src": "https://assets.pyecharts.org/assets/echarts.min.js"
            }
        )

    # 加入词云图依赖
    # 必须先加入ECHARTS依赖
    # 如已经添加则忽略
    def addEchartsWordCloud(self):
        if self.isTagExists("script", attributes={"id": "qv-echarts-wc-src"}):
            return

        if not self.isTagExists("script", {"id": "qv-echarts-src"}):
            raise RuntimeError("需要先导入echarts依赖")

        self.insertTagAfter(
            "script",
            "script",
            tagAttributes={"id": "qv-echarts-src"},
            newTagAttributes={
                "class": "qv",
                "id": "qv-echarts-wc-src",
                "type": "text/javascript",
                "src": "https://assets.pyecharts.org/assets/echarts-wordcloud.min.js"
            }
        )

    # 添加占位符
    def createPlaceHolder(self, tag):
        placeHolder = self.soup.new_tag("div", attrs={
            "class": "qv",
            "style": "display:none;",
            "place-holder": "true"
        })
        placeHolder.string = tag.prettify()

        tag.insert_after(placeHolder)

    # 删除标签并添加占位标签
    # 不能删除qv标签
    def delTag(self, tag):
        if "class" in tag.attrs and "qv" in tag.attrs["class"]:
            raise RuntimeError("不能删除qv标签")

        self.createPlaceHolder(tag)
        tag.decompose()

    # 引入资源冲突检测
    def checkConflict(self):
        for tag in self.iterTags("script"):

            if "class" in tag.attrs and "qv" in tag.attrs["class"]:
                continue

            # 处理echart和jquery的引用冲突
            if "src" in tag.attrs:
                if "echart" in tag.attrs["src"] or "jquery" in tag.attrs["src"]:
                    print("检测到冲突的资源引用: ", tag.prettify)

                    # todo: 仅实现覆盖冲突模式, 其他模式待实现
                    if self.conflictMode == ConflictMode.OVERWRITE:
                        self.delTag(tag)

    # 引入全部资源
    def loadResources(self):
        self.checkConflict()
        self.addJquery()
        self.addECharts()
        self.addEchartsWordCloud()

    # 回滚全部操作
    def rollBack(self):
        # 还原占位符
        for tag in self.iterTags("div", {"place-holder": "true"}):
            tag.insert_before(BeautifulSoup(tag.string, "html.parser"))

        # 删除class为qv的tag
        super(QVHtml, self).delTag(None, {"class": "qv"})

    # 修改指定div标签的ID
    # 添加占位符
    # 不能修改qv标签
    def changeDivID(self, id, newID, width=None, height=None):
        tag = self.soup.find("div", attrs={"id": id})

        if tag is None:
            raise RuntimeError("未找到id: %s" % id)

        if "class" in tag.attrs and "qv" in tag.attrs["class"]:
            raise RuntimeError("不能修改qv标签")

        self.createPlaceHolder(tag)

        tag.attrs["id"] = newID
        tag.attrs["class"] = "qv"

        if width is not None and height is not None:
            tag.attrs["style"] = "width: %s; height: %s" % (width, height)

    # 引入js文件
    # 需要先导入Echarts词云图依赖
    # 如果已经导入则忽略
    def loadJS(self, name):
        if self.isTagExists("script", attributes={"id": "qv-js-src-%s" % name}):
            return

        if not super(QVHtml, self).isTagExists("script", {"id": "qv-echarts-wc-src"}):
            raise RuntimeError("需要先导入Echarts词云图依赖")

        self.insertTagAfter(
            "script",
            "script",
            tagAttributes={"id": "qv-echarts-wc-src"},
            newTagAttributes={
                "class": "qv",
                "id": "qv-js-src-%s" % name,
                "type": "text/javascript",
                "src": "/static/qv/%s.js" % name
            }
        )



if __name__ == '__main__':
    html = QVHtml("E:\Projects\QuickVisual\demo.html")
    html.rollBack()
    html.save()
