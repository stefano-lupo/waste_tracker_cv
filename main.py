import sys
import cv2 as cv
import numpy as np

INGREDIENTS_BY_IMAGE = [
    {
        "filename": "img/plate.jpg",
        "ingredients": [
            {
                "name": "Carrot",
                "rgbMax": [235, 136, 62],
                "rgbMin": [190, 58, 36]
            },
            {
                "name": "Brocolli",
                "rgbMax": [155, 152, 42],
                "rgbMin": [78, 93, 19]
            },
            {
                "name": "Fish",
                "rgbMax": [217, 185, 162],
                "rgbMin": [196, 126, 77]
            }
        ]
    }, 
    {
        "filename": "img/steak_and_chips.jpeg",
        "ingredients": [
            {
                "name": "Steak",
                "rgbMax": [147, 78, 76],
                "rgbMin": [77, 41, 23]
            },
            {
                "name": "Chips",
                "rgbMax": [208, 175, 137],
                "rgbMin": [188, 123, 34],
            },
            {
                "name": "Salad",
                "rgbMax": [101, 150, 43],
                "rgbMin": [22, 72, 22],
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

def processFilter(frame, imageIngredient):
    ingredientName = imageIngredient["name"]

    # OpenCV uses BGR instead of RGB so need to reverse these
    bgrMin = imageIngredient["rgbMin"][::-1]
    bgrMax = imageIngredient["rgbMax"][::-1]
    
    rangeBottom = np.array(bgrMin, dtype = "uint8")
    rangeTop = np.array(bgrMax, dtype = "uint8")
    
    rgbStr = "(r:{0}, g:{1}, b:{2})"
    rangeBottomString = rgbStr.format(*bgrMin[::-1])
    rangeTopString = rgbStr.format(*bgrMax[::-1])
    print("%s: %s - %s" % (ingredientName, rangeBottomString, rangeTopString))
    
    mask = cv.inRange(frame, rangeBottom, rangeTop)
    res = cv.bitwise_and(frame, frame, mask=mask)
    cv.imshow(imageIngredient["name"], res) 

def processImg(imageIngredients):
    filename = imageIngredients["filename"]
    frame = cv.imread(filename, 1)
    print("Processing image %s" % filename)
    cv.imshow('Initial Dish', frame)

    for imageIngredient in imageDescription["ingredients"]:
        processFilter(frame, imageIngredient)

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
        print("No file specified")
    
    cv.destroyAllWindows()