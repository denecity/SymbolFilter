import cv2 as cv2
import numpy as np
from PIL import Image
from numba import jit
import math
import random
import os

imgSource = "6.jpg"
windowTitle = "Filter"
subFolder = "Symbol"
lowBallVal = 0
hiBallVal = 0
lowPassVal = 255
hiPassVal = 0


def lowBall(val):
    global lowBallVal
    lowBallVal = val
    restFilters()

def hiBall(val):
    global hiBallVal
    hiBallVal = val
    restFilters()

def lowPass(val):
    global lowPassVal
    lowPassVal = val
    restFilters()

def hiPass(val):
    global hiPassVal
    hiPassVal = val
    restFilters()


def scalePreview(img, maxWidth=1600, maxHeight=600): #1600 width or 600 height scaling
    origWidth = img.shape[1]
    origHeight = img.shape[0]
    ratio = maxWidth / maxHeight
    if origWidth / origHeight > ratio: #scale the width
        scale = maxWidth / origWidth
    elif origWidth / origHeight <= ratio: #scale the height
        scale = maxHeight / origHeight

    #print("origWidth:", origWidth, ", origHeight:", origHeight, ", scale:", scale)
    width = int(img.shape[1] * scale)
    height = int(img.shape[0] * scale)
    dim = (width, height)
    resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
    return resized

def restFilters():
    filtered = cv2.imread(imgSource, 0)
    cv2.namedWindow(windowTitle)

    _, thres = cv2.threshold(filtered, lowPassVal, 255, cv2.THRESH_TOZERO)
    thresInv = cv2.bitwise_not(thres)
    _, thres2 = cv2.threshold(thresInv, hiPassVal, 255, cv2.THRESH_TOZERO)
    thresNorm= cv2.bitwise_not(thres2)

    thresNorm[thresNorm == 0] = lowBallVal
    thresNorm[thresNorm == 255] = 255 - hiBallVal

    previewImg = scalePreview(thresNorm)
    cv2.imshow(windowTitle, previewImg)
    return previewImg

def symbolInit(img, margin=40):
    width = img.shape[1]
    height = img.shape[0]
    symImg = np.zeros((height + 2 * margin, width + 2 * margin))
    return symImg

def getRandomSymbol(subFolder): #need to get better symbol images
    numSymbols = len(os.listdir())
    randInd = random.randint(0, numSymbols - 1)
    symPath = "{}\\s{}.png".format(subFolder, randInd + 1)
    symbol = cv2.imread(symPath, 0)
    return symbol

@jit(nopython=True, parallel=True)
def createBrush(m, t, l, size, brush):
    for i in range(size[0]):
        for j in range(size[1]):
            x = ((m - i - 1)**2 + (m - j - 1)**2)**0.5
            brush[i][j] = int(t * (t / l) ** ((-1 * (x - m)**2)/(m**2)))
    return brush

def placeSymbol(img, pos, margin = 40): #place symbol on coordinate pos (center) on symImg
    symbol = getRandomSymbol(subFolder)
    symWidth = symbol.shape[1]
    symHeight = symbol.shape[0]

    startHeight = int(pos[0] + margin + symHeight / 2)
    startWidth = int(pos[1] + margin + symWidth / 2)
    
    img[startHeight:startHeight + symHeight, startWidth:startWidth + symWidth] = np.where(symbol > 200)

def subtractOrig(img, pos, brush): #subtract from orig image
    brush = createBrush()
    sizeX = brush.shape[0]
    sizeY = brush.shape[1]

    startHeight = int(pos[0] + sizeX / 2)
    startWidth = int(pos[1] + sizeY / 2)

    img[startHeight:startHeight + sizeX, startWidth:startWidth + sizeY]










    





cv2.namedWindow(windowTitle)
cv2.createTrackbar("Lowpass", windowTitle, 0, 255, hiPass)
cv2.createTrackbar("Lowball", windowTitle, 0, 255, hiBall)
cv2.createTrackbar("Hipass", windowTitle, 0, 255, lowPass)
cv2.createTrackbar("Hiball", windowTitle, 0, 255, lowBall)

restFilters()
cv2.waitKey()



"""
origImg = cv2.imread("8.jpg", 0)

symbolList = []

thres = 140
filterVal = 11 # redundant
sizeScale = 0.8
samples = 5000000
finalCircleSize = int(origImg.shape[1] / (100 * sizeScale))
finalCircleThicc = 2 #math.ceil(finalCircleSize / 5)
finalCircleAlpha = 0
circleStrength = 15
circleSize = math.ceil(finalCircleSize / 2)
endValue = 200

imgSize = (int(origImg.shape[1] / sizeScale), int(origImg.shape[0] / sizeScale))
origImg = cv2.resize(origImg, imgSize)
finImg = np.zeros(origImg.shape) + 255

origImg = np.where(origImg < thres, origImg * 0.7, 255)
#origImg = np.where(origImg < thres, 0, 255)

Image.fromarray(origImg).show()

for i in range(samples):
    nullImg = np.zeros(origImg.shape)
    #print(origImg)
    #Image.fromarray(origImg).show()

    #gaussImg = cv2.blur(origImg, (filterVal, filterVal), 0)
    gaussImg = origImg

    (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(gaussImg)
    if minVal > endValue:
        break
    #cv2.circle(gaussImg, minLoc, 50, (255, 0, 0), 2)

    circle = cv2.circle(nullImg, minLoc, circleSize, (circleStrength, circleStrength, circleStrength), 10)

    #cv2.circle(finImg, minLoc, finalCircleSize, (finalCircleAlpha, finalCircleAlpha, finalCircleAlpha, finalCircleAlpha), finalCircleThicc)
    symbolRand = symbolList[random.randint(0, 8)]
    try:
        finImg[minLoc[1]:minLoc[1]+symbolRand.shape[0], minLoc[0]:minLoc[0]+symbolRand.shape[1]] = np.where(symbolRand < 200, 0, finImg[minLoc[1]:minLoc[1]+symbolRand.shape[0], minLoc[0]:minLoc[0]+symbolRand.shape[1]])
    except:
        print("whoops")

    origImg = np.add(origImg, nullImg)

    #origImg = np.subtract(origImg, origImg)

    #Image.fromarray(gaussImg).show()
    #Image.fromarray(origImg).show()
    #Image.fromarray(nullImg).show()
    #Image.fromarray(subImg).show()
    #Image.fromarray(circle).show()
    if i % 500 == 0:
        #Image.fromarray(gaussImg).show()
        print(minVal)
        print(i)
    if i % 1000 == 0:
        #Image.fromarray(gaussImg).show()
        Image.fromarray(finImg).show()
    #print(i)

print("done")
Image.fromarray(finImg).show()
#Image.fromarray(nullImg).show()
"""