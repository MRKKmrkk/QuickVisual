# 数据输入输出格式


class InputFormat:

    def __init__(self, flag):
        self.flag = flag

    def generateReadCode(self):
        pass


class CSVInputFormat(InputFormat):

    def __init__(self, path):
        self.path = path
        self.flag = "csv"
        super(CSVInputFormat, self).__init__(self.flag)

    def generateReadCode(self):
        return """\ndef getData(path):
    return pandas.read_csv(path)\n\n"""

class SQLInputFormat(InputFormat):

    def __init__(self, host, user, password, db):
        self.host = host
        self.user = user
        self.password = password
        self.db = db
        self.flag = "sql"

        super(SQLInputFormat, self).__init__(self.flag)

    def generateReadCode(self):
        return """def getConnection():
    return pymysql.Connect(
        host="%s",
        user="%s",
        password="%s",
        db="%s"
    )\n
def getData(sql):
    return pandas.read_sql(sql, con=getConnection())\n\n""" % (self.host, self.user, self.password, self.db)

class OutputFormat:

    def __init__(self, flag):
        self.flag = flag

    def generateWriteCode(self):
        pass

class CSVOutputFormat(OutputFormat):

    def __init__(self, path):
        self.path = path
        self.flag = "csv"
        super(CSVOutputFormat, self).__init__(self.flag)

    def generateWriteCode(self):
        return """def saveData(path):
    return pandas.to_csv(path)\n"""

class SQLOutputFormat(OutputFormat):

    def __init__(self, host, user, password, db):
        self.host = host
        self.user = user
        self.password = password
        self.db = db
        self.flag = "sql"

        super(SQLOutputFormat, self).__init__(self.flag)

    def generateWriteCode(self):
        return """def saveData(df, table):
        return df.read_sql(table, con=create_engine(str(r"mysql+pymysql://%s:" + '%s' + "@%s/%s")))\n""" % (self.user, self.password, self.host, self.db)