from quickVisual import *

qv = QuickVisual(dataFrameFromCSV=False)

page = Page("index")
qv.addPage(page)

qv.generate()

