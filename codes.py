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
from pyecharts.charts import Pie, Bar, Line, Scatter
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
    return pandas.read_sql(sql, con=CONNECTION)\n"""