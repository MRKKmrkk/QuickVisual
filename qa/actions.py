from common.listUtil import coverToList

class Action:

    def __init__(self, name, dataFrom, dataOut, limit=None):
        self.name = name
        self.dataFrom = dataFrom
        self.dataOut = dataOut
        self.limit = limit

    def generateCode(self, content):
        limitLine = ""
        if self.limit is not None:
            if self.limit < 1:
                raise RuntimeError("limit不能小于1")

            limitLine = "df = df.iloc[:%s]" % str(self.limit + 1)

        return """
def %s():
    df = getData("%s")
    %s
    %s
    saveData(df, "%s")""" % (self.name, self.dataFrom, content, limitLine, self.dataOut)

class AggMode:
    AVG = "mean"
    SUM = "sum"
    COUNT = "count"

class GroupAction(Action):

    def __init__(self, groupKeys, aggKeys, aggMode, name, dataFrom, dataOut, limit=None):
        self.groupKeys = coverToList(groupKeys)
        self.aggKeys = coverToList(aggKeys)
        self.aggMode = aggMode
        super(GroupAction, self).__init__(name, dataFrom, dataOut, limit)

    def generateCode(self):
        return super(GroupAction, self).generateCode("""
    df.groupby(by=%s).%s()
    df = df[%s]""") % (str(self.groupKeys), self.aggMode, str(self.groupKeys + self.aggKeys))

if __name__ == '__main__':
    a = GroupAction("area", ["area", "num"], AggMode.AVG, "demo", "select * from a", "btable")
    print(a.generateCode())
