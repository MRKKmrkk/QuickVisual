import os
import random
import time
import turtle
import math

from win import screenCut

def leftConnect(height):
    turtle.right(90)
    turtle.forward(height / 2)
    turtle.left(90)

    pos = turtle.pos()
    x1 = 0
    y1 = height / 2
    x2 = pos[0]
    y2 = pos[1]

    t = abs(y2 - y1) / abs(x1 - x2)
    z = math.sqrt((y2 - y1) * (y2 - y1) + (x1 - x2) * (x1 - x2))
    turtle.right(math.atan(t) * (180 / math.pi))
    turtle.pendown()
    turtle.forward(z)
    turtle.penup()
    turtle.back(z)
    turtle.left(math.atan(t) * (180 / math.pi))

def rightConnect(height):
    turtle.right(90)
    turtle.forward(height / 2)
    turtle.right(90)

    pos = turtle.pos()
    x1 = 0
    y1 = height / 2
    x2 = pos[0]
    y2 = pos[1]

    t = abs(y2 - y1) / abs(x1 - x2)
    z = math.sqrt((y2 - y1) * (y2 - y1) + (x1 - x2) * (x1 - x2))
    turtle.left(math.atan(t) * (180 / math.pi))
    turtle.pendown()
    turtle.forward(z)
    turtle.penup()
    turtle.back(z)
    turtle.right(180 + math.atan(t) * (180 / math.pi))

def rectangle(pos, width, height, content=""):
    turtle.color("black")
    turtle.penup()
    turtle.goto(pos)

    turtle.forward(width / 2)
    turtle.left(90)

    turtle.pendown()
    turtle.forward(height / 2)

    turtle.left(90)
    turtle.forward(width)

    turtle.left(90)
    turtle.forward(height)

    turtle.left(90)
    turtle.forward(width)

    turtle.left(90)
    turtle.forward(height / 2)

    turtle.penup()
    turtle.goto(pos)
    turtle.left(180)
    turtle.forward(10)
    turtle.write(content, align="center", font=("宋体", 12, "normal"))

    turtle.left(180)
    turtle.forward(10)
    turtle.right(90)

def getLeftRectanglePos(width, interval, n):
    return 0 - interval / 2 - n * width - n * interval - width / 2

def getRightRectanglePos(width, interval, n):
    return interval / 2 + n * width + n * interval + width / 2

def drawER(entire, columns, width=140, height=90, xInterval=10, yInterval=None, pensize=1):
    if yInterval is None:
        yInterval = 2 * height

    turtle.clear()
    turtle.goto(0, 0)
    turtle.speed(0)
    turtle.pensize(pensize)

    rectangle(turtle.pos(), width, height, entire)

    li = 0
    ri = 0
    for i in range(len(columns)):
        if i % 2 == 0:
            rectangle((getLeftRectanglePos(width, xInterval, li), yInterval), width, height, columns[i])
            leftConnect(height)
            li += 1
        else:
            rectangle((getRightRectanglePos(width, xInterval, ri), yInterval), width, height, columns[i])
            rightConnect(height)
            ri += 1

    turtle.hideturtle()
    sc = screenCut()
    sc.save("%s属性实体图.png" % entire)

if __name__ == '__main__':
    drawER("用户", ["id", "姓名", "a", "b", "c", "a", "d"], pensize=2)
    # drawER("商品", ["id", "价格"])