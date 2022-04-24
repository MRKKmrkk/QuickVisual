class DataFormat:

    def __init__(self, flag):
        self.flag = flag

    def generateGetDataCode(self):
        pass

class SQLDataFormat(DataFormat):

    def __init__(self, host, user, password, databbase):
        self.host = host
        self.user = user
        self.password = password
        self.database = databbase
        self.flag = "sql"

        super(SQLDataFormat, self).__init__(self.flag)

    def generateGetDataCode(self):
        return """def getConnection():
    return pymysql.Connect(
        host="%s",
        user="%s",
        password="%s",
        db="%s"
    )\n
def getData(sql):
    return pandas.read_sql(sql, con=getConnection())\n""" % (self.host, self.user, self.password, self.database)

class CSVDataFormat(DataFormat):

    def __init__(self):
        self.flag = "csv"

        super(CSVDataFormat, self).__init__(self.flag)

    def generateGetDataCode(self):
        return """def getData(path):
    return pandas.read_csv(path)\n"""


if __name__ == '__main__':
    df = CSVDataFormat()
    print(df.generateGetDataCode())
    print(df.flag)

