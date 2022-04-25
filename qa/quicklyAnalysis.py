from common.pathUtils import checkDirectory
from qa.actions import GroupAction, AggMode
from qa.formats import SQLInputFormat, SQLOutputFormat


class QuicklyAnalysis:

    def __init__(self, projectPath, inputFormat, outputFormat):
        self.projectPath = projectPath
        if not checkDirectory(projectPath):
            raise RuntimeError("工程目录不存在: %s" % projectPath)

        self.inputFormat = inputFormat
        self.outputFormat = outputFormat

        self.actions = []

    def __addAction(self, action):
        self.actions.append(action)

    def addGroupAction(self, groupKeys, aggKeys, aggMode, name, dataIn, dataOut):
        self.__addAction(GroupAction(
            groupKeys,
            aggKeys,
            aggMode,
            name,
            dataIn,
            dataOut
        ))

    def generatePandasCode(self):
        pandasCode = """import pandas\nimport pymysql\nfrom sqlalchemy import create_engine\n\n"""
        pandasCode += self.inputFormat.generateReadCode()
        pandasCode += self.outputFormat.generateWriteCode()

        for action in self.actions:
            pandasCode += action.generateCode()

        with open(self.projectPath + "\\analysis.py", "w", encoding="utf-8") as f:
            f.write(pandasCode)


if __name__ == '__main__':
    # qa = QuicklyAnalysis("E:\Projects\QuickVisual", SQLInputFormat("host", "user", "pass", "db"), SQLOutputFormat("host", "user", "pass", "db"))
    # qa.addGroupAction("area", "num", AggMode.COUNT, "areaNumCount", "select * from data", "table")
    # qa.generatePandasCode(                )
    a = QuicklyAnalysis
    c = a("E:\Projects\QuickVisual", SQLInputFormat("host", "user", "pass", "db"),
          SQLOutputFormat("host", "user", "pass", "db"))
    c.generatePandasCode()
