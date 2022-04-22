PAGE_FLASK_CODE = """\n@app.route("/%s")
def %s():
    return render_template("%s.html")\n"""

PORT_JS_CODE = """\necharts.init(document.getElementById('%s')).dispose();
var %s = echarts.init(document.getElementById('%s'), 'white', {renderer: 'div'});
$.ajax({
    type: "GET",
    url: "http://127.0.0.1:5000/%s",
    dataType: 'json',
    success: function (result) {
       %s.setOption(result);
    }
});\n"""

PORT_JS_CODE2 = """\ntry {
    echarts.init(document.getElementById('%s')).dispose();
    var %s = echarts.init(document.getElementById('%s'), 'white', {renderer: 'div'});
    $.ajax({
        type: "GET",
        url: "http://127.0.0.1:5000/%s",
        dataType: 'json',
        success: function (result) {
           %s.setOption(result);
        }
    });
}
catch(err) {
    console.log(err.message);
}\n"""

PORT_CSS_CODE = """\n#%s {
    height: 400px;
    width: 400px;
}\n"""

PORT_FLASK_CODE_PIE = """\n@app.route("/%s")
def %s():
    df = getData("%s")

    pie = (
        Pie()
            .add("%s", [list(i) for i in zip(df['%s'].values.tolist(), df["%s"].values.tolist())])
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{d}%%"))
    )
    return Markup(pie.dump_options_with_quotes())\n"""

PORT_FLASK_CODE_BAR = """\n@app.route("/%s")
def %s():
    df = getData("%s")

    bar = (
        Bar()
            .add_xaxis(df['%s'].tolist())
            .add_yaxis("%s", df['%s'].tolist())
            .set_global_opts(
            yaxis_opts=opts.AxisOpts(name="%s"),
            xaxis_opts=opts.AxisOpts(name="%s", axislabel_opts={"rotate": 45}))
        .set_global_opts(datazoom_opts=opts.DataZoomOpts(
            range_start=40
        ))
    )
    return Markup(bar.dump_options_with_quotes())\n"""

PORT_FLASK_CODE_LINE = """\n@app.route("/%s")
def %s():
    df = getData("%s")

    line = (
        Line()
            .add_xaxis(df["%s"].values.tolist())
            .add_yaxis("%s", df["%s"].values.tolist())
            .set_global_opts(
            yaxis_opts=opts.AxisOpts(name="%s"),
            xaxis_opts=opts.AxisOpts(name="%s"))
    )
    return Markup(line.dump_options_with_quotes())\n"""

FLASK_INIT_CODE = """
import pandas
import pymysql
from flask import Flask, render_template, request, redirect, url_for
from pyecharts.charts import Pie, Bar, Line, Scatter, WordCloud
from pyecharts import options as opts
from jinja2 import Markup

app = Flask(__name__)
\n"""

DATAFRAME_FROM_CSV = """\ndef getData(path):
    return pandas.read_csv(path)\n"""

FLASK_END_CODE = """\n
if __name__ == '__main__':
    app.run(debug=True)\n"""

DATAFRAME_FROM_MYSQL = """\ndef getData(sql):
    return pandas.read_sql(sql, con=%s)\n"""

PORT_FLASK_CODE_WORDCLOUD = """@app.route("/%s")
def %s():
    df = getData("%s")
    
    words = df['%s'].tolist()
    nums = df['%s'].tolist()
    datas = []
    for i in range(len(words)):
        datas.append((words[i], nums[i]))
        
    c = (
        WordCloud()
        .add("", datas, word_size_range=[20, 100])
        .set_global_opts(title_opts=opts.TitleOpts(title="%s"))
    )
    return Markup(c.dump_options_with_quotes())\n"""

class ChartCode:

    def __init__(self, name, pathOrSql):
        self.name = name
        self.pathOrSql = pathOrSql

    def convertToList(self, l):
        if not isinstance(l, list):
            return [l]

        return l

    def generate(self, content, pre=""):
        return """\n@app.route("/%s")
def %s():
    df = getData("%s")
    %s
    c = (
        %s
    )
    return Markup(c.dump_options_with_quotes())\n""" % (self.name, self.name, self.pathOrSql, pre, content)

class BarCode(ChartCode):

    def __init__(self, name, xName, yNames, yDescs, xAxisName, yAxisName, pathOrSql):
        self.name = name
        self.xName = xName
        self.yNames = super(BarCode, self).convertToList(yNames)
        self.yDescs = super(BarCode, self).convertToList(yDescs)
        self.xAxisName = xAxisName
        self.yAxisName = yAxisName
        self.pathOrSql = pathOrSql
        super(BarCode, self).__init__(name, pathOrSql)

    def generate(self):
        content = """Bar()
            .add_xaxis(df['%s'].tolist())
            %s
            .set_global_opts(
            yaxis_opts=opts.AxisOpts(name="%s"),
            xaxis_opts=opts.AxisOpts(name="%s", axislabel_opts={"rotate": 45}))
            .set_global_opts(datazoom_opts=opts.DataZoomOpts(
            range_start=40
        ))"""

        if len(self.yNames) != len(self.yDescs):
            raise RuntimeError("yNames 的数量必须和 yDesc一致")

        addYaxis = [".add_yaxis(\"%s\", df['%s'].tolist())\n" % (self.yDescs[x], self.yNames[x]) for x in range(len(self.yDescs))]

        return super(BarCode, self).generate(
            content % (
                self.xName,
                "        ".join(addYaxis).strip(),
                self.yAxisName,
                self.xAxisName
            )
        )

class PieCode(ChartCode):

    def __init__(self, name, partName, partDesc, numName, pathOrSql):
        self.name = name
        self.partName = partName
        self.numName = numName
        self.pathOrSql = pathOrSql
        self.partDesc = partDesc

        super(PieCode, self).__init__(name, pathOrSql)

    def generate(self):
        return super(PieCode, self).generate(
            """Pie()
        .add("%s", [list(i) for i in zip(df['%s'].values.tolist(), df["%s"].values.tolist())])
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{d}%%"))""" % (self.partDesc, self.partName, self.numName)
        )

class LineCode(ChartCode):

    def __init__(self, name, xName, yNames, yDescs, xAxisName, yAxisName, pathOrSql):
        self.name = name
        self.xName = xName
        self.yNames = super(LineCode, self).convertToList(yNames)
        self.yDescs = super(LineCode, self).convertToList(yDescs)
        self.xAxisName = xAxisName
        self.yAxisName = yAxisName
        self.pathOrSql = pathOrSql
        super(LineCode, self).__init__(name, pathOrSql)

    def generate(self):

        if len(self.yNames) != len(self.yDescs):
            raise RuntimeError("yNames 的数量必须和 yDesc一致")

        addYaxis = [".add_yaxis(\"%s\", df['%s'].tolist())\n" % (self.yDescs[x], self.yNames[x]) for x in range(len(self.yDescs))]

        return super(LineCode, self).generate("""Line()
        .add_xaxis(df["%s"].values.tolist())
        %s
        .set_global_opts(
        yaxis_opts=opts.AxisOpts(name="%s"),
        xaxis_opts=opts.AxisOpts(name="%s"))""" % (self.xName, "        ".join(addYaxis).strip(), self.yAxisName, self.xAxisName))

class WordCloudCode(ChartCode):

    def __init__(self, name, wordName, numName, pathOrSql):
        self.name = name
        self.wordName = wordName
        self.numName = numName
        self.pathOrSql = pathOrSql

        super(WordCloudCode, self).__init__(name, pathOrSql)

    def generate(self):
        return super(WordCloudCode, self).generate("""WordCloud()
        .add("", datas, word_size_range=[20, 100])""", """\n    words = df['%s'].tolist()
    nums = df['%s'].tolist()
    datas = []
    for i in range(len(words)):
        datas.append((words[i], nums[i]))\n""")



if __name__ == '__main__':
    print(WordCloudCode("WordCloudCode", "words", "nums", "a.csv").generate())


