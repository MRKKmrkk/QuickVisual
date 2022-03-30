from codes import *
from bs4 import BeautifulSoup
from config import *


class Page:

    def __init__(self, name):
        self.name = name
        self.ports = []

        soup = BeautifulSoup(open(ROOT_PATH + "\\templates\\%s.html" % name, encoding="utf-8"), "html.parser")
        if not soup.find('div', attrs={'id': 'isInit'}):
            soup.find('body').insert(-1, soup.new_tag('div', attrs={'id': 'isInit'}))

            soup.find('head').insert(-1, soup.new_tag('script', attrs={'type': 'text/javascript', 'src': 'https://assets.pyecharts.org/assets/echarts.min.js'}))
            soup.find('head').insert(-1, soup.new_tag('script', attrs={'type': 'text/javascript', 'src': 'https://assets.pyecharts.org/assets/echarts-wordcloud.min.js'}))

            soup.find('body').insert(-1, soup.new_tag('script', attrs={'src': '/static/qv/jquery-3.3.1.min.js'}))
            soup.find('body').insert(-1, soup.new_tag('script', attrs={'src': '/static/qv/%s.js' % self.name}))
            soup.find('head').insert(-1, soup.new_tag('link', attrs={'href': '/static/qv/%s.css' % self.name, 'rel': 'stylesheet'}))
            with open(ROOT_PATH + "\\templates\\%s.html" % name, "w", encoding="utf-8") as f:
                f.write(soup.prettify())

    def addPort(self, port):
        self.ports.append(port)

    def generateFlaskCode(self):
        return PAGE_FLASK_CODE % (self.name, self.name, self.name)


class Port:

    def __init__(self, name, code):
        self.name = name
        self.code = code

    def generatorJSCode(self):
        return PORT_JS_CODE % (self.name, self.name, self.name, self.name, self.name)

    def generateFlaskCode(self):
        return self.code.generate()


class PiePort(Port):

    def __init__(self, name, partName, partDesc, numName, pathOrSql):
        self.name = name
        self.code = PieCode(name, partName, partDesc, numName, pathOrSql)
        super(PiePort, self).__init__(name, self.code)


class BarPort(Port):

    def __init__(self,  name, xName, yNames, yDescs, xAxisName, yAxisName, pathOrSql):
        self.name = name
        self.code = BarCode(name, xName, yNames, yDescs, xAxisName, yAxisName, pathOrSql)
        super(BarPort, self).__init__(name, self.code)

class LinePort(Port):

    def __init__(self, name, xName, yNames, yDescs, xAxisName, yAxisName, pathOrSql):
        self.name = name
        self.code = LineCode(name, xName, yNames, yDescs, xAxisName, yAxisName, pathOrSql)
        super(LinePort, self).__init__(name, self.code)


class CloudWord(Port):

    def __init__(self, name, wordName, numName, pathOrSql):
        self.name = name
        self.code = WordCloudCode(name, wordName, numName, pathOrSql)
        super(CloudWord, self).__init__(name, self.code)

