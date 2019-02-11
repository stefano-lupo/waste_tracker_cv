import numpy as np
import cv2 as cv

def scalePercentTo(perc, scaleTo):
    return (perc / 100) * scaleTo  


# Open CV uses h[0-180], s[0-255], v[0-255]
def hsvAnglePercentToHSV(hsv):
    hAct = hsv[0] / 2
    sAct = (hsv[1] / 100) * 255
    vAct = (hsv[2] / 100) * 255
    return np.array([hAct, sAct, vAct])

def toPixel(bgr):
    return np.uint8([[bgr]])

def bgrToHsv(bgrFrame):
    hsv = cv.cvtColor(bgrFrame, cv.COLOR_BGR2HSV)
    return hsv