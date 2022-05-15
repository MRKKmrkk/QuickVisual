from bs4 import BeautifulSoup

'''
冲突模式
'''
class ConflictMode:
    # 覆盖
    OVERWRITE = "overwrite"

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

    #创建标签
    def createTag(self, name, attrs, content):
        tag = self.soup.new_tag(name, attrs=attrs)
        if content is None:
            tag.string = ""
        else:
            tag.string = content
        return tag

'''
基于QV业务的HTML编辑功能
'''
class QVHtml(HTML):

    def __init__(self, modelPath, outPath, encoding="utf-8"):
        self.modelPath = modelPath
        self.outPath = outPath
        self.encoding = encoding
        self.soup = BeautifulSoup(open(modelPath, encoding=encoding), "html.parser")

        # 冲突映射
        self.ConflictMap = {
            "echarts": ConflictMode.OVERWRITE,
            "jquery": ConflictMode.KEEP
        }

    # 保存html文件
    def save(self):
        with open(self.outPath, "w", encoding="utf-8") as f:
            f.write(self.soup.prettify())   

    # 冲突检测
    def _checkConflict(self):
        for tag in self.iterTags("script"):                                                                 

            # 处理echart和jquery的引用冲突
            if "src" in tag.attrs:
                for source in self.ConflictMap:
                    if source in tag.attrs["src"]:
                        if self.ConflictMap[source] == ConflictMode.OVERWRITE:
                            print("检测到冲突的资源引用, 正在删除: ", tag.prettify)
                            tag.decompose()
                            break
                        if self.ConflictMap[source] == ConflictMode.KEEP:
                            print("检测到冲突的资源引用, 已保留: ", tag.prettify)
                            tag.attrs["qv-conflitct-mode"] = "keep"
                            break


    # 加载JQuery
    def _addJQuery(self):
        if self.isTagExists("script", attributes={"qv-conflitct-mode": "keep"}):
            return

        self.insertTagIn(
            "body",
            "script",
            -1,
            newTagAttributes={
                "id": "qv-jquery-src",
                "type": "text/javascript",
                "src": "https://cdn.bootcss.com/jquery/3.3.1/jquery.min.js"
            }
        )

    # 加入Echarts依赖
    # 由于默认删除冲突依赖，这里不做检测
    def _addECharts(self):

        self.insertTagIn(
            "body",
            "script",
            -1,
            newTagAttributes={
                "id": "qv-echarts-src",
                "type": "text/javascript",
                "src": "https://assets.pyecharts.org/assets/echarts.min.js"
            }   
        )   

    # 加入词云图依赖
    # 由于默认删除冲突依赖，这里不做检测
    def _addEchartsWordCloud(self):
        
        self.insertTagIn(
            "body",
            "script",
            -1,
            newTagAttributes={
                "id": "qv-echarts-wc-src",
                "type": "text/javascript",
                "src": "https://assets.pyecharts.org/assets/echarts-wordcloud.min.js"
            }
        )


    # 加载资源
    def loadResource(self):
        self._checkConflict()
        self._addJQuery()
        self._addECharts()
        self._addEchartsWordCloud()

if __name__ == '__main__':
    html = QVHtml("demo.html", "out.html")
    html.loadResource()
    html.save()    
