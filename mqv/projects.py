from mqv.codes import PAGE_FLASK_CODE, PieCode, BarCode, LineCode, WordCloudCode, PORT_JS_CODE4


class Page:

    def __init__(self, name, isIndex):
        self.name = name
        self.ports = []
        self.isIndex = isIndex

    def addPort(self, port):
        self.ports.append(port)

    def generateFlaskCode(self):
        return PAGE_FLASK_CODE % (self.name, self.name, self.name)

class Port:

    def __init__(self, name, desc, code):
        self.name = name
        self.code = code
        self.desc = desc

    def generatorJSCode(self):
        return PORT_JS_CODE4 % (self.name, self.name, self.name, self.name)

    def generateFlaskCode(self):
        return self.code.generate()

class PiePort(Port):

    def __init__(self, name, desc, partName, partDesc, numName, pathOrSql):
        self.name = name
        self.code = PieCode(name, partName, partDesc, numName, pathOrSql)
        super(PiePort, self).__init__(name, desc, self.code)


class BarPort(Port):

    def __init__(self, name, desc, xName, yNames, yDescs, xAxisName, yAxisName, pathOrSql):
        self.name = name
        self.code = BarCode(name, xName, yNames, yDescs, xAxisName, yAxisName, pathOrSql)
        super(BarPort, self).__init__(name, desc, self.code)

class LinePort(Port):

    def __init__(self, name, desc, xName, yNames, yDescs, xAxisName, yAxisName, pathOrSql):
        self.name = name
        self.code = LineCode(name, xName, yNames, yDescs, xAxisName, yAxisName, pathOrSql)
        super(LinePort, self).__init__(name, desc, self.code)


class CloudWord(Port):

    def __init__(self, name, desc, wordName, numName, pathOrSql):
        self.name = name
        self.code = WordCloudCode(name, wordName, numName, pathOrSql)
        super(CloudWord, self).__init__(name, desc, self.code)
