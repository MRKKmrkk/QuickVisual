from qe.draw import drawER


class Column:

    def __init__(self, fieldName, desc, fieldType, isNone, isPrimaryKey, default):
        self.fieldName = fieldName
        self.desc = desc
        self.type = fieldType
        self.isNone = isNone
        self.isPrimaryKey = isPrimaryKey
        self.default = default

    def __str__(self):
        return "|" + "|".join([
            self.fieldName,
            self.desc,
            self.type,
            self.isNone,
            self.isPrimaryKey,
            self.default
        ]) + "|"


class Table:

    def __init__(self, tableName, tableDesc):
        self.tableName = tableName
        self.tableDesc = tableDesc
        self.columns = []

    def getDescs(self):
        return [x.desc for x in self.columns]

    def addColumn(self, fieldName, desc, fieldType, isNone, isPrimaryKey, default):
        self.columns.append(Column(
            fieldName,
            desc,
            fieldType,
            isNone,
            isPrimaryKey,
            default
        ))

    def generateMarkDownCode(self):
        descs = self.getDescs()
        startCode = "\n\n%s表共有%d个字段,分别是：" % (self.tableDesc, len(descs)) + "、".join(
            descs) + "。具体表字段如下表所示:\n\n" + "|字段名|解释|类型|是否允许为空|是否为主键|默认值|\n" + "|" + "|".join(
            [":-:" for x in range(6)]) + "|\n"

        for column in self.columns:
            startCode += str(column) + "\n"
        return startCode

    def getTableInfoDoc(self):
        doc = "=====%s:%s=====\n" % (self.tableName, self.tableDesc)
        for column in self.columns:
            doc += ",".join([
                column.fieldName,
                column.desc,
                column.type,
                column.isNone,
                column.isPrimaryKey,
                column.default
            ]) + "\n"
        doc += "==============\n"
        return doc


    def generateER(self):
        drawER(
            self.tableName,
            self.getDescs()
        )

if __name__ == '__main__':
    table = Table("index", "所有")
    table.addColumn(Column("a", "a", "int", "yes", "yes", "1"))
    table.addColumn(Column("a", "a", "int", "yes", "yes", "1"))
    print(table.generateMarkDownCode())

