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
            soup.find('body').insert(-1, soup.new_tag('script', attrs={'src': '/static/qv/jquery-3.3.1.min.js'}))
            soup.find('body').insert(-1, soup.new_tag('script', attrs={'src': '/static/qv/echarts.js'}))
            soup.find('body').insert(-1, soup.new_tag('script', attrs={'src': '/static/qv/%s.js' % self.name}))
            with open(ROOT_PATH + "\\templates\\%s.html" % name, "w", encoding="utf-8") as f:
                f.write(soup.prettify())

    def addPort(self, port):
        self.ports.append(port)

    def generateFlaskCode(self):
        return PAGE_FLASK_CODE % (self.name, self.name, self.name)


class Port:

    def __init__(self, name):
        self.name = name
        self.type = type

    def generatorJSCode(self):
        return PORT_JS_CODE % (self.name, self.name, self.name, self.name, self.name)


class PiePort(Port):

    def __init__(self, name, partsName, partDesc, valuesName, path):
        self.partsName = partsName
        self.valuesName = valuesName
        self.path = path
        self.partDesc = partDesc
        super(PiePort, self).__init__(name)

    def generateFlaskCode(self):
        return PORT_FLASK_CODE_PIE % (self.name, self.name, self.path, self.partDesc, self.partsName, self.valuesName)


class BarPort(Port):

    def __init__(self, name, xName, xDesc, yDesc, yName, path):
        self.xName = xName
        self.yName = yName
        self.xDesc = xDesc
        self.yDesc = yDesc
        self.path = path
        super(BarPort, self).__init__(name)

    def generateFlaskCode(self):
        return PORT_FLASK_CODE_BAR % (
        self.name, self.name, self.path, self.xName, self.yDesc, self.yName, self.yDesc, self.xDesc)


class LinePort(Port):

    def __init__(self, name, xName, xDesc, yDesc, yName, path):
        self.xName = xName
        self.yName = yName
        self.xDesc = xDesc
        self.yDesc = yDesc
        self.path = path
        super(LinePort, self).__init__(name)

    def generateFlaskCode(self):
        return PORT_FLASK_CODE_LINE % (
            self.name,
            self.name,
            self.path,
            self.xName,
            self.yDesc,
            self.yName,
            self.yDesc,
            self.xDesc
        )


if __name__ == '__main__':
    Page("index")
