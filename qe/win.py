import sys

import win32con
import win32gui
from PIL import ImageGrab


def getWinPos():
    handler = win32gui.FindWindow(0, "Python Turtle Graphics")
    if handler == 0:
        return None
    else:
        return win32gui.GetWindowRect(handler), handler

def screenCut():
    handler = win32gui.FindWindow(0, "Python Turtle Graphics")
    (x1, y1, x2, y2), handler = getWinPos()
    win32gui.SendMessage(handler, win32con.WM_SYSCOMMAND, win32con.SC_RESTORE, 0)
    win32gui.SetForegroundWindow(handler)
    grab_image = ImageGrab.grab((x1 + 100, y1 + 100, x2 - 100, y2 - 100))
    return grab_image
