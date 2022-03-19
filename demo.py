from pyecharts.charts import Bar, Line
from pyecharts import options as opts

from quickVisual import *

qv = QuickVisual()

p = Page("index")
p.addPort(BarPort(
    "demoBar",
    "type",
    ["num1", "num2"],
    ["数量1", "数量2"],
    "种类",
    "数量",
    "demo.csv"
))

qv.addPage(p)

qv.generate()
