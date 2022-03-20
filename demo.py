from pyecharts.charts import Bar, Line
from pyecharts import options as opts

from quickVisual import *


# clean()

qv = QuickVisual()

index = Page("index")
index.addPort(BarPort(
    "courseMean",
    "course",
    "avg",
    "品均分",
    "课程",
    "品均分",
    "../data2/courseMean.csv"
))
index.addPort(BarPort(
    "courseLevel",
    "course",
    ["不及格", "良", "优"],
    ["不及格", "良", "优"],
    "课程",
    "数量",
    "../data2/courseLevel.csv"
))
index.addPort(LinePort(
    "groupMean",
    "group",
    ["math", "reading", "writing"],
    ["math", "reading", "writing"],
    "小组",
    "平均分",
    "../data2/groupMean.csv"
))
index.addPort(PiePort(
    "lunchFailCount",
    "lunch",
    "餐饮标准",
    "count",
    "../data2/lunchFailCount.csv"
))

index.addPort(PiePort(
    "genderFailCount",
    "gender",
    "性别",
    "count",
    "../data2/genderFailCount.csv"
))

index.addPort(LinePort(
    "parentEduMean",
    "parentEdu",
    ["math", "reading", "writing"],
    ["math", "reading", "writing"],
    "父母教育水平",
    "平均分",
    "../data2/parentEduMean.csv"
))

qv.addPage(index)

qv.addPage(Page("login"))

qv.generate()