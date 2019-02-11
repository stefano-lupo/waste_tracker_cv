import sys
import cv2 as cv
import numpy as np

# cap = cv.VideoCapture(0)

HUE_SPREAD = 10
SATURATION_SPREAD = 255
VALUE_SPREAD = 255


def scalePercentTo(perc, scaleTo):
    return (perc / 100) * scaleTo  

# Open CV uses h[0-180], s[0-255], v[0-255]
def hsvAnglePercentToHSV(hsv):
    hAct = hsv[0] / 2
    sAct = scalePercentTo(hsv[1], 255)
    vAct = scalePercentTo(hsv[2], 255)
    return np.array([hAct, sAct, vAct])


def toPixel(rgb):
    return np.uint8([[rgb]])

def rgbToHsv(rgbPixel):
    hsv = cv.cvtColor(rgbPixel, cv.COLOR_BGR2HSV)
    # print("RGB: " + str(rgbPixel) + " --> HSV: " + str(hsv))
    return hsv


INGREDIENTS_BY_IMAGE = [
    {
        "filename": "img/plate.jpg",
        "ingredients": [
            {
                "name": "Carrot",
                "bgrMax": [43, 150, 101],
                "bgrMin": [22, 72, 22],
                "actualHsv": [20, 89.85, 77.25]
            },
            {
                "name": "Brocolli",
                "bgrMax": [43, 150, 101],
                "bgrMin": [22, 72, 22],
                "actualHsv": [68, 80.15, 51.37]
            }
        ]
    }, 
    {
        "filename": "img/steak_and_chips.jpeg",
        "ingredients": [
            {
                "name": "Steak",
                "bgrMax": [76, 78, 147],
                "bgrMin": [23, 41, 77],
                "actualHsv": [16.67, 46.15, 45.88]
            },
            {
                "name": "Chips",
                "bgrMax": [137, 175, 208],
                "bgrMin": [34, 123, 188],
                "actualHsv": [32.93, 61.57, 84.71]
            },
            {
                "name": "Salad",
                "bgrMax": [43, 150, 101],
                "bgrMin": [22, 72, 22],
                "actualHsv": [119.28, 51.9, 33]
            }
        ]
    }
]

def waitForKeyPress():
    k = cv.waitKey(5) & 0xFF
    if k != None and k == 120:
        print(k)
        return True
    return False

def processFilter(frame, frameHsv, imageIngredient):
     # define range of blue color in HSV
    # medianHsv = rgbToHsv(toPixel(highLow["medianRgb"]))[0][0]
    # print("Median HSV: ", medianHsv)
    # rangeBottom = np.array([medianHsv[0]-30, 50, 50])
    # rangeTop = np.array([medianHsv[0]+30, 255, 255])
    
    actualHsv = hsvAnglePercentToHSV(imageIngredient["actualHsv"])
    bgrMin = imageIngredient["bgrMin"]
    bgrMax = imageIngredient["bgrMax"]
    
    rangeTop = np.array(actualHsv)
    # rangeTop = rangeTop + [HUE_SPREAD, SATURATION_SPREAD, VALUE_SPREAD]
    # rangeTop[0] = rangeTop[0] + COLOUR_SPREAD
    # rangeTop[1] = rangeTop[1]
    # rangeTop[2] = 255

    rangeBottom = np.array(actualHsv)
    # rangeTop = rangeTop + [HUE_SPREAD, SATURATION_SPREAD, VALUE_SPREAD]
    # rangeBottom[0] = rangeBottom[0] - COLOUR_SPREAD
    # rangeBottom[1] = 100
    # rangeBottom[2] = 100

    rangeBottom = np.array(bgrMin, dtype = "uint8")
    rangeTop = np.array(bgrMax, dtype = "uint8")

    print("\n" + imageIngredient["name"])
    print("range bottom: ", rangeBottom)
    print("range top: ", rangeTop)
    # print("highRgb: ", highRgb)
    # print("lowRgb: ", lowRgb)
    # print(frameHsv)
    
    # Threshold the HSV image to get only blue colors
    mask = cv.inRange(frameHsv, rangeBottom, rangeTop)
    # print(mask)
    # print(lowRgb)
    # print(highRgb)
    # print(frameHsv)

    # Bitwise-AND mask and original image
    res = cv.bitwise_and(frame,frame, mask=mask)
    # cv.imshow('mask',mask)
    cv.imshow(imageIngredient["name"],res)


def processFrame(frame, imageDescription):
     # Convert BGR to HSV
    # frameHsv = rgbToHsv(frame)
    cv.imshow('frame',frame)

    for imageIngredient in imageDescription["ingredients"]:
        processFilter(frame, frame, imageIngredient)

# def processCam():
#     while 1:
#         # Take each frame
#         _, frame = cap.read()

#         processFrame(frame)   

#         if waitForKeyPress():
#             break
  

def processImg(imageIngredients):
    frame = cv.imread(imageIngredients["filename"], 1)
    processFrame(frame, imageIngredients)

    while (1):
        if (waitForKeyPress()):
            return

if (__name__ == "__main__"):
    if (len(sys.argv) > 1):
        filename = sys.argv[1]
        for imageDescription in INGREDIENTS_BY_IMAGE:
            if (imageDescription["filename"] != filename):
                continue
            
            processImg(imageDescription)
            exit
        print("Unable to find image ingredient data for %s", filename)
    else:
        processCam()
    
    cv.destroyAllWindows()